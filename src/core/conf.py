from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlite_file_name: str = "database.db"
    database_url: str = f"sqlite:///{sqlite_file_name}"
    access_token_expire_minutes: int = 100


settings = Settings()