import logging
import os
from core.settings.app import AppSettings

f = open("core/settings/env.txt", "r")
lines = f.readlines()


class DevAppSettings(AppSettings):
    debug: bool = True
    minio_endpoint: str = "10.255.187.41:9000"
    minio_access_key: str = "minio"
    minio_secret_key: str = "minio123"
    data_bucket_name: str = "upload-images"
    pipeline_id: str = os.environ.get("pipeline_id") if os.environ.get("pipeline_id") else lines[0].strip()
    user_id: str = os.environ.get("user_id")
    project_id: str = os.environ.get("project_id")
    dataset_version_id: str = os.environ.get("dataset_id") if os.environ.get("dataset_id") else lines[1].strip()
    logging_level: int = logging.DEBUG
    f.close()

    class Config(AppSettings.Config):
        env_file = "dev.env"
