from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    staff = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=True)
    image = models.ImageField(default='/avatar.jpg', upload_to='Profile_Images')       #NAPRAWIC TE AVATARY (NIE MOGE OGARNAC
                                                                                                #O CO CHODZI Z TYMI ICONAMI AVATAROW)

    def __str__(self):
        return f'{self.staff.username}-Profile'