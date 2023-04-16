from fastaws import S3Client
from fastpg import Database

from .settings import settings

database = Database(
    user=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    database=settings.POSTGRES_DB,
)

s3_client = S3Client(
    access_key=settings.WASABI_ACCESS_KEY,
    secret_key=settings.WASABI_SECRET_KEY,
    region=settings.WASABI_REGION,
    provider="wasabisys",
)
