from app.core.config import settings
from app.core.types import FileStorageType
from app.core.file_storage.engines import BaseFSEngine
from app.core.file_storage.engines.CloudFSEngine import CloudFSEngine
from app.core.file_storage.engines.LocalFSEngine import LocalFSEngine


class FileStorageService:
    engine: BaseFSEngine = None
    bucket: str = None

    def __init__(self):
        if settings.FS_TYPE == FileStorageType.LOCAL:
            self.engine = LocalFSEngine()
        if settings.FS_TYPE == FileStorageType.SBER:
            self.engine = CloudFSEngine()

    def get_dict(self, filename, bucket: str = settings.S3_BUCKET_NAME):
        file = self.engine.get_file(bucket=bucket, filename=filename)
        return file

    def update_dict(self, file_data, filename, bucket: str = settings.S3_BUCKET_NAME):
        file = self.engine.update_file(file=file_data, bucket=bucket, filename=filename)
        return file

    def save_dict(self, file_data, filename, bucket: str = settings.S3_BUCKET_NAME):
        file = self.engine.save_file(file=file_data, bucket=bucket, filename=filename)
        return file

    def save_file(self, file_data, bucket, filename):
        return self.engine.save_file(file=file_data, bucket=bucket, filename=filename)

    def delete_file(self, bucket, filename):
        return self.engine.delete_file(bucket=bucket, filename=filename)

    def get_list(self, bucket):
        return self.engine.get_list(bucket=bucket)


fs_service = FileStorageService()
