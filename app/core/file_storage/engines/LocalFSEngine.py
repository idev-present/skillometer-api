import os.path
from pathlib import Path

from app.core.config import settings
from app.core.file_storage.engines import BaseFSEngine


class LocalFSEngine(BaseFSEngine):
    def __init__(self):
        parent_dir = Path(settings.LOG_DIR)
        self.root_path = os.path.join(parent_dir.parent.absolute(), 'data')
        if not os.path.exists(self.root_path):
            os.mkdir(self.root_path)

    def save_file(self, file: bytes | str, bucket, filename):
        filepath = os.path.join(self.root_path, bucket)
        if isinstance(file, str):
            file_bytes = str.encode(file, 'utf-8')
        else:
            file_bytes = file
        output_file = Path(os.path.join(filepath, filename))
        output_file.parent.mkdir(exist_ok=True, parents=True)
        f = open(output_file, 'wb')
        f.write(file_bytes)
        f.close()
        return str(filename)

    def get_file(self, bucket, filename):
        filepath = os.path.join(self.root_path, bucket)
        try:
            f = open(os.path.join(filepath, filename), 'rb')
            file = f.read()
            f.close()
            return file
        except FileNotFoundError:
            return None

    def delete_file(self, bucket, filename):
        filepath = os.path.join(self.root_path, bucket)
        os.remove(os.path.join(filepath, filename))

    # def get_upload_link(self, bucket, filename):
    #     return {
    #         "fields": {
    #             "key": "internal"
    #         },
    #         "url": f"{settings.API_BASE_URL}/pool/upload?filename={filename}"
    #     }
    #
    # def get_download_link(self, bucket, filename):
    #     return f"{settings.API_BASE_URL}/static/{filename}"
