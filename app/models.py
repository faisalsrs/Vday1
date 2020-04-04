from django.db import models
from django.contrib import messages
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def validator(self, data):
        errors = {}
        if len(data['fname']) < 2:
            errors['fname'] = "Name must be more than 2 characters"
        if len(data['lname']) < 2:
            errors['lname'] = "Name must be more than 2 characters"
        if not EMAIL_REGEX.match(data['email']):
            errors['email'] = "Email is invalid"
        if len(data['password']) < 5:
            errors['password'] = "Password needs to be 5 characters or longer"
        return errors


class GiftManager(models.Manager):
    def validator(self, data):
        errors = {}
        if len(data['item']) < 2:
            errors['item'] = "Item needs 3 chars and more"
        if (data['description']) == "":
            errors['description'] = "Description cannot be empty"
        if data['item_url'] == "":
            errors['item'] = "Must have item url"
        if not EMAIL_REGEX.match(data['email2']):
            errors['email2'] = "Email is invalid"
        return errors


class GrantorManager(models.Manager):
    def validator(self, data):
        errors = {}
        if not EMAIL_REGEX.match(data['email2']):
            errors['email2'] = "Email is invalid"
        return errors


class User(models.Model):
    email = models.CharField(max_length=60)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Gift(models.Model):
    item = models.CharField(max_length=50)
    grantor = models.ManyToManyField("User", related_name="sugar")
    item_url = models.TextField()
    email2 = models.CharField(max_length=60)
    granted_item = models.BooleanField(default=False)
    description = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_by = models.ForeignKey(
        'User', on_delete='CASCADE', related_name="gifts")
    objects = GiftManager()
    objects2 = GrantorManager()
