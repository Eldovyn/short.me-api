from dotenv import load_dotenv
import os

load_dotenv()

database_mongodb = os.getenv("DATABASE_MONGODB")
database_mongodb_url = os.getenv("DATABASE_MONGODB_URL")
salt_account_active_email = os.getenv("SALT_ACCOUNT_ACTIVE_EMAIL")
secret_key_account_active_email = os.getenv("SECRET_KEY_ACCOUNT_ACTIVE_EMAIL")
salt_account_active_web = os.getenv("SALT_ACCOUNT_ACTIVE_WEB")
secret_key_account_active_web = os.getenv("SECRET_KEY_ACCOUNT_ACTIVE_WEB")
api_key_google_trends = os.getenv("API_KEY_GOOGLE_TRENDS")
api_key_apify = os.getenv("API_KEY_APIFY")
smtp_host = os.getenv("SMTP_HOST")
smtp_port = os.getenv("SMTP_PORT")
smtp_email = os.getenv("SMTP_EMAIL")
smtp_password = os.getenv("SMTP_PASSWORD")
celery_broker_url = os.getenv("CELERY_BROKER_URL")
celery_result_backend = os.getenv("CELERY_RESULT_BACKEND")
client_id_google = os.getenv("CLIENT_ID_GOOGLE")
client_secret_google = os.getenv("CLIENT_SECRET_GOOGLE")
