from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User)
    mobile = models.IntegerField()
    newsletter = models.BooleanField(default=0)
    book_count = models.IntegerField(default=0)
    last_visited = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user.username