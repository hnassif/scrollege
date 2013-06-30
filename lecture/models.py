from django.db import models
from django.contrib.auth.models import User
from teach2me.settings import MEDIAFILES_DIRS
from taggit.managers import TaggableManager


# Create your models here.

# class School(models.Model):
#    name = models.CharField(max_length=100)


class Course(models.Model):
    name = models.CharField(max_length=255)
    c_id = models.CharField(max_length=30)
    instructor = models.ForeignKey(User)
    # institution = models.ForeignKey(School)

    def __str__(self):
        return str(self.c_id) + ', ' + str(self.name)


class Item(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    name= models.CharField(max_length=200)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    negotiable = models.BooleanField(default=False)
    owner=models.ForeignKey(User)
    description = models.CharField(max_length=2000)
    tags = TaggableManager()

    def __str__(self):
            return str(self.name) + ', ' + str(self.description) + \
            str(self.tags.all())

