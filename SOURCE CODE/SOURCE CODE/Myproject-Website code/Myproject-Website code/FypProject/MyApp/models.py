from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Type(models.Model):
    Rname = models.CharField(max_length=120)

    def __str__(self):
        return self.Rname


class Hotels(models.Model):
    name = models.CharField('Hotel Name', max_length=120)
    description = models.TextField()
    image = models.ImageField(upload_to='hotel_images')
    types = models.ManyToManyField(Type, related_name='types')
    address = models.CharField('Address', max_length=100, default='kathmandu')
    favourite = models.ManyToManyField(User, related_name='favourite', blank=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    hotels = models.ForeignKey(Hotels,default = 1, on_delete=models.CASCADE)
    user = models.ForeignKey(User,default = 1, on_delete=models.CASCADE)
    content = models.TextField(max_length=160)
    rating = models.IntegerField(default = 1)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.hotels.name, str(self.user.username))

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.user.username