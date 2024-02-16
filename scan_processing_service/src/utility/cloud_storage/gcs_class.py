import os
import pathlib
import mimetypes
from google.cloud import storage
import decouple
import loguru
from functools import lru_cache

STORAGE_CLASSES = ("STANDARD", "NEARLINE", "COLDLINE", "ARCHIVE")

os.environ["GCLOUD_PROJECT"] = "scan-processing"

working_dir = pathlib.Path.cwd()
downloads_folder = working_dir.joinpath("downloads")


class GCStorage:
    def __init__(self, storage_client):
        self.client = storage_client

    def get_bucket(self, bucket_name, project_id):
        return self.client.bucket(bucket_name, user_project=project_id)

    def list_buckets(self):
        buckets = self.client.list_buckets()
        return [bucket.name for bucket in buckets]

    def download_blob(self, bucket_name, blob_name, project_id):
        try:
            bucket = self.get_bucket(bucket_name, project_id=project_id)
            blob = bucket.blob(blob_name)
            path_download = downloads_folder.joinpath(blob.name)
            if not path_download.parent.exists():
                path_download.parent.mkdir(parents=True)
            blob.download_to_filename(str(path_download))
            return path_download
        except Exception as e:
            raise e


# @lru_cache()
# def get_gcstorage() -> GCStorage:
#
#     return GCStorage(client)


@lru_cache()
def get_gcstorage() -> GCStorage:
    try:
        client = storage.Client()

    except Exception:
        loguru.logger.error(
            "Failed to authenticate with Google Cloud Storage by loading credentials from fiele. Trying to authenticate with environment variables."
        )
        client = storage.Client.from_service_account_info(
            {
                "type": os.environ.get("GCLOUD_TYPE"),
                "project_id": os.environ.get("GCLOUD_PROJECT_ID"),
                "private_key_id": os.environ.get("GCLOUD_PRIVATE_KEY_ID"),
                "private_key": os.environ.get("GCLOUD_PRIVATE_KEY"),
                "client_email": os.environ.get("GCLOUD_CLIENT_EMAIL"),
                "client_id": os.environ.get("GCLOUD_CLIENT_ID"),
                "auth_uri": os.environ.get("GCLOUD_AUTH_URI"),
                "token_uri": os.environ.get("GCLOUD_TOKEN_URI"),
                "auth_provider_x509_cert_url": os.environ.get("GCLOUD_AUTH_PROVIDER_CERT_URL"),
                "client_x509_cert_url": os.environ.get("GCLOUD_CLIENT_CERT_URL"),
            }
        )

    return GCStorage(client)


gcstorage: GCStorage = get_gcstorage()
