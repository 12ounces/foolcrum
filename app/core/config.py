from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = 'postgresql+asyncpg://postgres:6425@localhost:5432/foolcrum_db'
    secret_key: str = 'secret'
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 30

    class Config:
        env_file = '.env'


settings = Settings()
