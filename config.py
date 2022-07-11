import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class ApiConfig:
    API_KEY = os.environ.get("API_KEY")

    SESSION_COOKIE_NAME = os.environ.get(
        "SESSION_ID_COOKIE_NAME") or "session_id"

    SIGN_STATES = bool(os.environ.get("SIGN_STATES"))

    SECRET_KEY = os.environ.get("SECRET_KEY")

    if SIGN_STATES and not SECRET_KEY:
        raise Exception("To use sign states you need to set a secret_key")

    PRODUCTION = os.environ.get("PRODUCTION")
    RELOAD_API = True if not PRODUCTION else False

    if not os.environ.get("CORS_ALLOWED_ORIGINS"):
        CORS_ALLOWED_ORIGINS = ["*"]
    else:
        origins = os.environ.get("CORS_ALLOWED_ORIGINS").split(",")
        CORS_ALLOWED_ORIGINS = [
            origin.strip()
            for origin
            in origins
            if origin
        ]

    if not os.environ.get("SERVER_SECURE_PROTOCOL"):
        SERVER_PROTOCOL = "http"
    else:
        SERVER_PROTOCOL = "https"
    SERVER_HOST = os.environ.get("SERVER_HOST") or "localhost"
    SERVER_PORT = int(os.environ.get("SERVER_PORT") or 8000)

    SERVER_ORIGIN = f"{SERVER_PROTOCOL}://{SERVER_HOST}:{SERVER_PORT}"


class DatabaseSSLConfig:
    CERTIFICATE_FILE_PATH = os.environ.get(
        "DATABASE_SSL_CERTIFICATE_FILE_PATH")
    KEY_FILE_PATH = os.environ.get("DATABASE_SSL_KEY_FILE_PATH")
    PASSWORD = os.environ.get("DATABASE_SSL_PASSWORD")


class DatabaseConfig:

    HOST = os.environ.get("DATABASE_HOST")
    if os.environ.get("DATABASE_PORT"):
        PORT = int(os.environ.get("DATABASE_PORT"))
    else:
        PORT = None
    NAME = os.environ.get("DATABASE_NAME")
    USERNAME = os.environ.get("DATABASE_USERNAME")
    PASSWORD = os.environ.get("DATABASE_PASSWORD")
    USE_SSL = bool(os.environ.get("DATABASE_USE_SSL"))
