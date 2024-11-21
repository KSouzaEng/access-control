from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_URL: str
    DB_URL: str
    DEPLOYMENT_ENVIRONMENT: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

settings = Settings()
