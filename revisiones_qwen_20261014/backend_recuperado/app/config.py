from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus

class Settings(BaseSettings):
    PROJECT_NAME: str = "AC-ICEN propuesta Qwen"
    VERSION: str = "2.8.0-propuesta"
    API_V1_STR: str = "/api/v1"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "icen_d04c"
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)
    @property
    def DATABASE_URL(self) -> str:
        user = quote_plus(self.POSTGRES_USER)
        password = quote_plus(self.POSTGRES_PASSWORD)
        return f"postgresql+psycopg2://{user}:{password}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()
