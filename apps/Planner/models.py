from __future__ import unicode_literals
from django.utils.safestring import mark_safe
from calendar import HTMLCalendar
from django.urls import reverse
import calendar
from datetime import datetime as dt
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def new_validator(self, postData):
        errors = {}
        if len(postData['fname']) < 2:
            errors['fname'] = 'First name is too short, has to be 2 characters and more'
        if not postData['fname'].isalpha():
            errors['digit'] = 'Cannot enter a digit in the name fields'
        if len(postData['lname']) < 2:
            errors['lname'] = 'Last name is too short, has to be 2 characters and more'
        if not postData['lname'].isalpha():
            errors['digit'] = 'Cannot enter a digit in the name fields'
        if len(postData['email']) < 2:
            errors['email'] = 'Email is too short'
        elif not EMAIL_REGEX.match(postData['email']):
            errors['regex'] = 'Email isnt valid, enter the email again'
        try:
            if User.objects.get(email=postData['email']):
                errors['unique'] = 'User aleady exist, please log in'
            if len(postData['password']) < 4:
                errors['password'] = 'Password has to be more than 4 characters'
            if postData['password'] != postData['passwordc']:
                errors['match'] = 'The passwords do not match, please try again!'
        except:
            if len(postData['password']) < 4:
                errors['password'] = 'Password has to be more than 4 characters'
            if postData['password'] != postData['passwordc']:
                errors['match'] = 'The passwords do not match, please try again!'
        return errors

    def log_validator(self, postData):
        errors = {}
        user = ""
        email = postData['lemail']
        password = postData['lpassword']
        try:
            user = User.objects.get(email=email)
            if not user.email == email:
                errors['nouser'] = 'Login error'
            if not bcrypt.checkpw(password.encode(), user.password.encode()):
                errors['password'] = 'Login error'
        except:
            errors["error"] = "Login error"
        return errors

    def event_validator(self, postData):
        errors = {}
        title = postData['title']
        start = postData['start']
        end = postData['end']
        notes = postData['notes']
        if len(title)==0:
            errors['title'] = "title is too short<br>"
        today = dt.today()
        if start == "":
            errors['date'] = 'date not valid <br>'
            return errors
        if end == "":
            errors['date'] = 'date not valid<br>'
            return errors
        start_dt = dt.strptime(start, '%Y-%m-%dT%H:%M')
        end_dt = dt.strptime(end, '%Y-%m-%dT%H:%M')
        if start_dt<today:
            errors['start'] = 'start value invalid<br>'
        if end_dt<start_dt:
            errors['end'] = 'end date is invalid<br>'
        return errors



class User(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    start_month = models.IntegerField()
    start_year = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.id+" " + self.fname + " " + self.email

class Profile(models.Model):
    image = models.ImageField(upload_to='apps/Planner/static/images/', default='media/default.jpg')
    bio = models.TextField(blank=True)
    updated_at = models.DateField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.fname} Profile'

class Post(models.Model):
    text = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    post_commented = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class Event(models.Model):
    title = models.CharField(max_length=100)
    end = models.DateTimeField()
    start = models.DateTimeField()
    notes = models.TextField()
    user_created = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = UserManager()

    def __str__(self):
        return self.title + " " + self.notes

