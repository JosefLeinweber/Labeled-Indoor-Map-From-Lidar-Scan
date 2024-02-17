import os
import pathlib
from google.cloud import storage
import loguru
import pathlib
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


@lru_cache()
def get_gcstorage() -> GCStorage:
    try:
        loguru.logger.debug(f"Trying to authenticate with Google Cloud Storage")
        client = storage.Client()
        loguru.logger.info("Authenticated with Google Cloud Storage")
        return GCStorage(client)
    except Exception as e:
        loguru.logger.error(f"Failed to authenticate with Google Cloud Storage: {e}")
        raise e


gcstorage: GCStorage = get_gcstorage()
