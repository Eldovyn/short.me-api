import authlib.integrations
import authlib.integrations.base_client
from flask import Flask, request, url_for, jsonify
import os
from .config import (
    database_mongodb,
    database_mongodb_url,
    smtp_host,
    smtp_port,
    smtp_email,
    smtp_password,
    celery_broker_url,
    celery_result_backend,
    client_id_google,
    client_secret_google,
)
from .database import db
from .celery_app import celery_init_app
from .mail import mail
import datetime
from .models import AccountActiveModel
from celery.schedules import crontab
from authlib.integrations.flask_client import OAuth
import authlib
from google.oauth2 import id_token
from google.auth.transport import requests


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    private_key_path = os.path.join(BASE_DIR, "keys", "private.pem")
    public_key_path = os.path.join(BASE_DIR, "keys", "public.pem")

    oauth = OAuth(app)
    google = oauth.register(
        name="google",
        client_id=client_id_google,
        client_secret=client_secret_google,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid profile email"},
    )

    global PRIVATE_KEY, PUBLIC_KEY
    with open(private_key_path, "rb") as f:
        PRIVATE_KEY = f.read()

    with open(public_key_path, "rb") as f:
        PUBLIC_KEY = f.read()

    app.config.from_prefixed_env()
    app.config.from_mapping(
        CELERY=dict(
            broker_url=celery_broker_url,
            result_backend=celery_result_backend,
            task_ignore_result=True,
        ),
    )
    app.secret_key = client_secret_google
    app.config["MONGODB_SETTINGS"] = {
        "db": database_mongodb,
        "host": database_mongodb_url,
        "connect": False,
    }
    app.config["MAIL_SERVER"] = smtp_host
    app.config["MAIL_PORT"] = smtp_port
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False
    app.config["MAIL_USERNAME"] = smtp_email
    app.config["MAIL_PASSWORD"] = smtp_password
    app.config["MAIL_DEFAULT_SENDER"] = smtp_email

    global celery_app
    celery_app = celery_init_app(app)
    db.init_app(app)
    mail.init_app(app)

    @celery_app.task(name="delete_token_task")
    def delete_token_task():
        expired_at = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
        if data_account_active := AccountActiveModel.objects.all():
            for account_active_data in data_account_active:
                if account_active_data.expired_at <= expired_at:
                    account_active_data.delete()
        return f"delete token at {int(datetime.datetime.now(datetime.timezone.utc).timestamp())}"

    celery_app.conf.beat_schedule = {
        "run-every-5-minutes": {
            "task": "delete_token_task",
            "schedule": crontab(minute="*/5"),
        },
    }

    with app.app_context():
        from .api.register import register_router
        from .api.login import login_router

        app.register_blueprint(login_router)
        app.register_blueprint(register_router)

    @app.get("/login/google")
    def login_google():
        token = request.args.get("token")
        try:
            # Specify the WEB_CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                "113118193592-loc110rrqru2gmg3ahr94771n1c7hp8j.apps.googleusercontent.com",
            )

            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [WEB_CLIENT_ID_1, WEB_CLIENT_ID_2, WEB_CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            # If the request specified a Google Workspace domain
            # if idinfo['hd'] != DOMAIN_NAME:
            #     raise ValueError('Wrong domain name.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            userid = idinfo["sub"]  # Google user ID
            email = idinfo.get("email")
            name = idinfo.get("name")
            picture = idinfo.get("picture")

            print("User ID:", userid)
            print("Email:", email)
            print("Name:", name)
            print("Picture:", picture)

            return jsonify(
                {"userid": userid, "email": email, "name": name, "picture": picture}
            )
        except Exception as e:
            print(e)
            return "ValueError"

    @app.route("/authorize/google")
    def authorize_google():
        try:
            token = google.authorize_access_token()
            userinfo_endpoint = google.server_metadata["userinfo_endpoint"]
            resp = google.get(userinfo_endpoint)
            user_info = resp.json()
            print(token)
            return "user_info"
        except authlib.integrations.base_client.errors.MismatchingStateError:
            return "MismatchingStateError"

    @app.after_request
    async def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = (
            "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        )
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

    @app.before_request
    def before_request():
        request.timestamp = datetime.datetime.now(datetime.timezone.utc)

    return app
