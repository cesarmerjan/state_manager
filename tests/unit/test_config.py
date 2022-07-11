from config import DatabaseConfig, DatabaseSSLConfig, ApiConfig


def test_database_config():
    assert hasattr(DatabaseConfig, "HOST")
    assert hasattr(DatabaseConfig, "PORT")
    assert hasattr(DatabaseConfig, "NAME")
    assert hasattr(DatabaseConfig, "USERNAME")
    assert hasattr(DatabaseConfig, "PASSWORD")
    assert hasattr(DatabaseConfig, "USE_SSL")


def test_database_ssl_config():
    assert hasattr(DatabaseSSLConfig, "CERTIFICATE_FILE_PATH")
    assert hasattr(DatabaseSSLConfig, "KEY_FILE_PATH")
    assert hasattr(DatabaseSSLConfig, "PASSWORD")


def test_api_config():
    assert hasattr(ApiConfig, "API_KEY")
    assert hasattr(ApiConfig, "SESSION_COOKIE_NAME")
    assert hasattr(ApiConfig, "SIGN_STATES")
    assert hasattr(ApiConfig, "SECRET_KEY")
    assert hasattr(ApiConfig, "PRODUCTION")
    assert hasattr(ApiConfig, "RELOAD_API")
    assert hasattr(ApiConfig, "CORS_ALLOWED_ORIGINS")
    assert hasattr(ApiConfig, "SERVER_PROTOCOL")
    assert hasattr(ApiConfig, "SERVER_HOST")
    assert hasattr(ApiConfig, "SERVER_PORT")
    assert hasattr(ApiConfig, "SERVER_ORIGIN")
