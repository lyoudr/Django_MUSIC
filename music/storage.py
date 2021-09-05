
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from storages.backends.s3boto3 import S3Boto3Storage

class LocalStaorge(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(location = settings.MEDIA_ROOT)



class RemoteStorage(S3Boto3Storage):
    def __init__(self, *args, **kwargs):
        super().__init__(bucket_name = settings.AWS_STORAGE_BUCKET_NAME, *args, **kwargs)


def select_storage():
    print(settings.ENV)
    return LocalStaorge() if settings.ENV == 'local' else RemoteStorage()