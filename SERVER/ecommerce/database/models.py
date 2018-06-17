from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=16, null=True)
    sex = models.CharField(max_length=5, null=True)
    birthday = models.DateField(null=True)
    address = models.TextField(null=True)
    city = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=20, null=True)
    zip_code = models.CharField(max_length=20, null=True)
    additional_info = models.TextField(null=True)
    phone_number = models.CharField(max_length=20, null=True)


class Product(models.Model):
    title = models.TextField(null=False)
    url = models.URLField(null=True)
    photo = models.URLField(null=True)
    category = models.TextField(null=True)
    price = models.CharField(max_length=20)
    star = models.CharField(max_length=20)
    description = models.TextField(null=True)
    details = models.TextField(null=True)


class UserProd(models.Model):
    user_info = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
