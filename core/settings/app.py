import logging
from core.settings.base import BaseAppSettings


class AppSettings(BaseAppSettings):
    debug: bool = False

    max_connection_count: int = 10
    min_connection_count: int = 10

    minio_endpoint: str = "10.255.187.41:9000"
    minio_access_key: str = "minio"
    minio_secret_key: str = "minio123"
    data_bucket_name: str = "upload-images"
    pipeline_id: str
    user_id: str
    project_id: str
    dataset_version_id: str

    logging_level: int = logging.INFO

    class Config:
        validate_assignment = True
