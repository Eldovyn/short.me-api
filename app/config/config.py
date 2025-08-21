from dotenv import load_dotenv
import os

load_dotenv()

database_mongodb = os.getenv("DATABASE_MONGODB")
database_mongodb_url = os.getenv("DATABASE_MONGODB_URL")
salt_account_active = os.getenv("SALT_ACCOUNT_ACTIVE")
secret_key_account_active = os.getenv("SECRET_KEY_ACCOUNT_ACTIVE")
salt_reset_password = os.getenv("SALT_RESET_PASSWORD")
secret_key_reset_password = os.getenv("SECRET_KEY_RESET_PASSWORD")
smtp_host = os.getenv("SMTP_HOST")
smtp_port = int(os.getenv("SMTP_PORT", 587))
smtp_email = os.getenv("SMTP_EMAIL")
smtp_password = os.getenv("SMTP_PASSWORD")
celery_broker_url = os.getenv("CELERY_BROKER_URL")
celery_result_backend = os.getenv("CELERY_RESULT_BACKEND")
celery_url = os.getenv("CELERY_URL")
web_short_me = os.getenv("WEB_SHORT_ME")
provider = os.getenv("PROVIDER")
cloudinary_api_secret = os.getenv("CLOUDINARY_API_SECRET")
cloudinary_api_key = os.getenv("CLOUDINARY_API_KEY")
cloudinary_cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")

