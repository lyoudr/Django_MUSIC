
from django.conf import settings
from django.core.files.storage import FileSystemStorage

class LocalStaorge(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(location = settings.MEDIA_ROOT)


class RemoteStorage:
    pass


def select_storage():
    return LocalStaorge() if settings.ENV == 'local' else RemoteStorage()