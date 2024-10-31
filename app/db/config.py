from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    DB_USERNAME: Optional[str]
    DB_PASSWORD: Optional[str]
    DB_HOST: Optional[str] = "localhost"
    DB_PORT: Optional[int] = 5432
    DB_NAME: Optional[str]

    DB_URL: Optional[str] = None

    @property
    def DATABASE_URL(self) -> str:

        if self.DB_URL:
            return self.DB_URL
        
        if not all([self.DB_USERNAME, self.DB_PASSWORD, self.DB_NAME]):
            raise ValueError(
                "Missing database configuration set appropriate values in .env file."
            )
                
        return f"postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore'
    )


Config = Settings()