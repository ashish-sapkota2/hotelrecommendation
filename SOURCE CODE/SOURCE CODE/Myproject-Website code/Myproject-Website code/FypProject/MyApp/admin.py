from django.contrib import admin
from MyApp import models
from .models import Hotels, Type, Comment, Profile
# Register your models here.

admin.site.register(Hotels)
admin.site.register(Type)
admin.site.register(Profile)
admin.site.register(Comment)
