from typing import Literal

from pydantic import BaseSettings


class Settings(BaseSettings):
    OS_ENV: Literal["host"] | Literal["docker"]
    BUILD_ENV: Literal["development"] | Literal["production"]

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    PLUGIN_HOSTNAME: str

    MAPBOX_TOKEN: str

    WASABI_ACCESS_KEY: str
    WASABI_SECRET_KEY: str
    WASABI_REGION: str

    OPENAI_API_KEY: str

    PINECONE_ENVIRONMENT = "us-central1-gcp"
    PINECONE_API_KEY = "a1ceaa4c-f65e-4f48-9919-e4ac441edb36"


settings = Settings()  # pyright: ignore
