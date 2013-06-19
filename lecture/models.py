from django.db import models
from django.contrib.auth.models import User
from teach2me.settings import MEDIAFILES_DIRS

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
	item_name= models.CharField(max_length=200)
	item_type=models.CharField(max_length=10)
	# item_image=models.ImageField(upload_to=MEDIAFILES_DIRS)
	item_owner=models.ForeignKey(User)
	item_description= models.CharField(max_length=2000)

	def __str__(self):
        	return str(self.item_name) + ', ' + str(self.item_type)

