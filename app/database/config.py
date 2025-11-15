from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Global application configuration.
    Loads environment variables safely using pydantic-settings.
    """

    DATABASE_URL: str = "sqlite:///./academic.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
