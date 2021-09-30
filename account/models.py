from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserRole(models.Model):
    class Meta:
        db_table = 'USER_ROLE'
        
    ROLES = [
        (1, 'admin'),
        (2, 'manager'),
        (3, 'normal_member'),
        (4, 'vip_member')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.IntegerField(
        choices = ROLES,
    )

    def __str__(self):
        return f'role_{self.role}'