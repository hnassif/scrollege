from django.db import models
from django.contrib.auth.models import User
# from teach2me.settings import MEDIAFILES_DIRS
from taggit.managers import TaggableManager
import hashlib



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
    image = models.FileField(upload_to='documents/%Y/%m/%d',
        blank=True)
    tags = TaggableManager()

    def __str__(self):
            return str(self.pk)+' '+str(self.name) + ', ' + str(self.description) + \
            str(self.tags.all())


class Message(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=2000)
    sender = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    isRead = models.BooleanField(default=False)

    def __str__(self):
            return 'From : ' +  str(self.sender) + ' Subject : ' + str(self.content) + ' time : ' + str(self.timestamp)

    def jOb(self):
        return {
            'timestamp':str(self.timestamp),
            'from':self.sender.first_name+' '+self.sender.last_name,
            'message':self.content,
            'read':self.isRead,
            'email':hashlib.md5(self.sender.email).hexdigest(),
            'subject':self.item.name,
            'price': self.item.price,
            'description':self.item.description,
            'item_id':self.item.pk,
            'sender_id':self.sender.pk
        }
        

