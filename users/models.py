from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import os

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User)
    mobile = models.BigIntegerField()
    newsletter = models.BooleanField(default=0)
    item_count = models.IntegerField(default=0)
    last_visited = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user.username


class Item(models.Model):
    student = models.ForeignKey(Student)
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=100, null=True, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    item_type = models.CharField(max_length=15)
    image = models.ImageField(upload_to='images', default='no-image.png')
    thumbnail = models.ImageField(upload_to='images', blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(default=datetime.now)
    sold = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.title

    def create_thumbnail(self):
        if not self.image:
            return

        from PIL import Image
        from django.core.files.uploadhandler import BytesIO
        from django.core.files.uploadedfile import SimpleUploadedFile

        THUMBNAIL_SIZE = (150, 195)
        FULL_SIZE = (760, 950)

        DJANGO_TYPE = self.image.file.content_type

        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'
        elif DJANGO_TYPE == 'image/gif':
            PIL_TYPE = 'gif'
            FILE_EXTENSION = 'gif'
        elif DJANGO_TYPE == 'image/jpg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'

        r = BytesIO(self.image.read())
        fullsize_image = Image.open(r)
        new_image = fullsize_image.copy()

        fullsize_image.thumbnail(FULL_SIZE, Image.ANTIALIAS)

        temp_handle = BytesIO()
        fullsize_image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1], temp_handle.read(), content_type=DJANGO_TYPE)

        self.image.save('{}.{}'.format(os.path.splitext(suf.name)[0], FILE_EXTENSION), suf, save=False)

        new_image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        temp_handle = BytesIO()
        new_image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1], temp_handle.read(), content_type=DJANGO_TYPE)

        self.thumbnail.save('{}_thumbnail.{}'.format(os.path.splitext(suf.name)[0], FILE_EXTENSION), suf, save=False)

    def save(self):
        self.create_thumbnail()
        super(Item, self).save()