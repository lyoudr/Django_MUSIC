
from django.conf import settings
from django.core.files.storage import FileSystemStorage

class LocalStaorge(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(location = settings.MEDIA_ROOT)


class RemoteStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(location = '/tmp/media/') # need to put to cloud


def select_storage():
    return LocalStaorge() if settings.ENV == 'local' else RemoteStorage()