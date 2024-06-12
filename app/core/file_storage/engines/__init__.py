class BaseFSEngine:

    def get_file(self, bucket, filename):
        raise NotImplementedError

    def save_file(self, file, bucket, filename):
        raise NotImplementedError

    def update_file(self, file, bucket, filename):
        raise NotImplementedError

    def delete_file(self, bucket, filename):
        raise NotImplementedError

    def get_list(self, bucket):
        raise NotImplementedError
