import io

import boto3
from botocore.exceptions import ClientError
from starlette.datastructures import UploadFile
from structlog import get_logger

from app.core.config import settings
from app.core.exceptions import ServerError
from app.core.file_storage.engines import BaseFSEngine

logger = get_logger(__name__)


class CloudFSEngine(BaseFSEngine):
    session: boto3.session.Session = None
    client = None

    def __init__(self):
        self.session = boto3.session.Session(
            aws_access_key_id=f'{settings.S3_TENANT_ID}:{settings.S3_API_KEY}',
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name="ru-central-1"
        )
        self.client = self.session.client(
            service_name='s3',
            endpoint_url=settings.S3_ENDPOINT
        )

    async def save_file(self, file: bytes | str | UploadFile, bucket, filename):
        if isinstance(file, str):
            file_bytes = io.BytesIO(str.encode(file, 'utf-8'))
        if isinstance(file, UploadFile):
            file_bytes = io.BytesIO(await file.read())
        else:
            file_bytes = io.BytesIO(file)

        try:
            result = self.client.upload_fileobj(Fileobj=file_bytes, Bucket=bucket, Key=filename)
            logger.info(result)
            return result
        except ClientError as e:
            logger.error(e)
            message = "Ошибка при попытке загрузки файла в хранилище"
            logger.error(message)
            raise ServerError(message=e.response['Error']['Message'])

    def update_file(self, file: bytes | str, bucket, filename):
        if isinstance(file, str):
            file_bytes = io.BytesIO(str.encode(file, 'utf-8'))
        else:
            file_bytes = io.BytesIO(file)

        try:
            result = self.client.put_object(Body=file_bytes, Bucket=bucket, Key=filename)
            return result
        except ClientError as e:
            logger.error(e)
            message = "Ошибка при попытке загрузки файла в хранилище"
            logger.error(message)
            raise ServerError(message)

    def get_file(self, bucket, filename):
        try:
            result = self.client.get_object(Bucket=bucket, Key=filename)
            body = result.get('Body')
            return body.read()
        except (
                ClientError,
                AttributeError
        ) as e:
            logger.error(e)
            message = "Ошибка при чтении файла в хранилище"
            logger.error(message)
            raise ServerError(message)

    def get_upload_link(self, bucket, filename):
        try:
            result = self.client.generate_presigned_post(Bucket=bucket, Key=filename)
            return result
        except ClientError as e:
            logger.error(e)
            message = "Ошибка при генерации ссылки для загрузки"
            logger.error(message)
            raise ServerError(message)

    def get_list(self, bucket):
        return [key for key in self.client.list_objects(Bucket=bucket)['Contents']]
