from django.db import models
from music.storage import select_storage


class SysPhoto(models.Model):
    class Meta:
        db_table = 'SYS_PHOTO'
    
    image = models.FileField(upload_to = 'sys_photos', storage = select_storage)

    def __str__(self):
        return self.image.name

    def delete(self):
        super(SysPhoto, self).delete()
        self.image.delete(save = True)



class SysSheet(models.Model):
    class Meta:
        db_table = 'SYS_SHEET'
    
    sheet = models.FileField(upload_to = 'sys_sheets', storage = select_storage)

    def __str__(self):
        return self.sheet.name