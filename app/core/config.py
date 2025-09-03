import os
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv


# Detecta el archivo .env según APP_ENV
app_env = os.getenv("APP_ENV", "dev")
env_file = ".env.test" if app_env == "test" else ".env"

# 👇 Cargamos el .env adecuado ANTES de inicializar Settings
load_dotenv(env_file, override=True)


class Settings(BaseSettings):
    # Variables de PostgreSQL
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # Propiedad para construir DATABASE_URL
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Variables JWT
    JWT_SECRET: str = Field(default="change-me")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_MINUTES: int = 60

    # Otras variables
    APP_ENV: str = app_env
    LOG_LEVEL: str = "INFO"

    model_config = {
        "env_file": env_file,
        "env_file_encoding": "utf-8",
        "extra": "ignore",  # Ignorar variables adicionales
    }


settings = Settings()

print(f"✅ Usando configuración desde {env_file}, DB={settings.DATABASE_URL}")
