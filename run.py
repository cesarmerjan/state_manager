import uvicorn
from src.api import create_api
from config import ApiConfig, DatabaseConfig
from src.database import Database


database_config = {
    "host": DatabaseConfig.HOST,
    "port": DatabaseConfig.PORT,
    "database": DatabaseConfig.NAME,
    "use_ssl": DatabaseConfig.USE_SSL
}


database = Database("redis", database_config)
database.connect(DatabaseConfig.USERNAME,
                 DatabaseConfig.PASSWORD)

api = create_api(
    api_key=ApiConfig.API_KEY,
    database=database,
    session_cookie_name=ApiConfig.SESSION_COOKIE_NAME,
    sign_state=ApiConfig.SIGN_STATES,
    secret_key=ApiConfig.SECRET_KEY,
    # servers=[{
    #     "url": ApiConfig.SERVER_ORIGIN
    # }]
)


if __name__ == "__main__":
    uvicorn.run("run:api", host="0.0.0.0", port=ApiConfig.SERVER_PORT,
                reload=ApiConfig.RELOAD_API, workers=1)
