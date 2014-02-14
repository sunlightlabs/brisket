import datetime

from storages.backends.s3boto import S3BotoStorage
from django.core.files.storage import get_storage_class
from django.conf import settings


class CachedS3BotoStorage(S3BotoStorage):
    """
    S3 storage backend that saves the files locally, too.
    """
    def __init__(self, *args, **kwargs):
        super(CachedS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def modified_time(self, name):
        # try to get mtime from local cache before calling out over S3
        try:
            return self.local_storage.modified_time(name)
        # if the file isn't there, we need to copy
        except:
            return datetime.datetime(1900, 1, 1)

    def save(self, name, content):
        name = super(CachedS3BotoStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name

StaticRootS3BotoStorage = lambda: CachedS3BotoStorage(
    location='{prefix}static'.format(prefix=settings.AWS_PREFIX))
MediaRootS3BotoStorage = lambda: S3BotoStorage(
    location='{prefix}media'.format(prefix=settings.AWS_PREFIX))
