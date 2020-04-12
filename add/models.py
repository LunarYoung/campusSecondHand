from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class Yzm(models.Model):
    yzm = models.IntegerField(default=0)



class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=20)
    i_code = models.CharField(unique=False, blank=True, max_length=10)
    email = models.EmailField(unique=False, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'person_info'


class upthing(models.Model):
    id = models.AutoField(primary_key=True)
    Thing_own = models.CharField(max_length=30)
    image = models.ImageField(upload_to='img')
    image1 = models.ImageField(upload_to='img')
    link = models.CharField(max_length=100)
    price = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    dtail = models.TextField(max_length=400)
    data = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'thing_info'

class upneed(models.Model):
    id = models.AutoField(primary_key=True)
    upName = models.CharField(max_length=30)
    name = models.CharField(unique=False, max_length=30)
    price = models.CharField(unique=False, max_length=20)
    link = models.CharField(max_length=100)
    dTail = models.TextField(max_length=400)
    data = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'upNeed_info'




@receiver(pre_delete, sender=upthing)
def mymodel_delete(sender, instance, **kwargs):
    instance.image.delete(False)
    instance.image1.delete(False)

