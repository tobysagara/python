from __future__ import unicode_literals
from django.db import models
import re, bcrypt
# Create your models here.
class UserManager(models.Manager):
     def create_validator(self, request_POST):
          EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
          errors = {}
          if len(request_POST['first_name']) < 2:
               errors['first_name'] = "Firstname must be longer than 2 characters."
          if len(request_POST['last_name']) < 2:
               errors['last_name'] = "Last name must be longer than 2 characters."
          if len(request_POST['email']) < 8:
               errors['email'] = "email must be longer than 8 characters."
          if len(request_POST['password']) < 8:
               errors['password'] = "Password must be longer than 8 characters."
          if request_POST['password'] != request_POST['password_confirmation']:
               errors['password_confirmation'] = "Password confirmation does not match Password."
          if not EMAIL_REGEX.match(request_POST['email']):
               errors['regex'] = "email is not in correct format."
          return errors

class User(models.Model):
     first_name = models.CharField(max_length=45)
     last_name = models.CharField(max_length=45)
     email = models.CharField(max_length=45)
     password = models.TextField()
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     objects = UserManager()

class WishManager(models.Manager):
     def wish_validator(self, postData):
          errors = {}

          if len(postData['name']) < 3:
               errors['name'] = 'name must be at least 3 characters'
          if len(postData['description']) < 5:
               errors['description'] = 'Description must be at least 3 characters'

          return errors

class Wish(models.Model):
     granted = models.ManyToManyField(User, related_name="granted")
     name = models.CharField(max_length=255)
     creator = models.ForeignKey(User, related_name="wishes_made", on_delete=models.CASCADE)
     description = models.CharField(max_length=255)
     created_at = models.DateField(auto_now_add=True)
     updated_at = models.DateField(auto_now=True)
     objects = WishManager()