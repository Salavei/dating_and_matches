from django.db import models


class Photo(models.Model):
    name = models.CharField(max_length=200, null=False)
    photo = models.ImageField(upload_to='register_photo', null=False)

    def __str__(self):
        return self.name

