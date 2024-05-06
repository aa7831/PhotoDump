from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.conf import settings
import os


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    hometown = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'dob', 'hometown']

    def __str__(self):
        return self.email

class Friend(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="friends_set1")
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="friends_set2")

    class Meta:
        unique_together = (('user1', 'user2'),)

    def __str__(self):
        return f"{self.user1.email} and {self.user2.email} are friends"
    
class Album(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='albums')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} owned by {self.owner}"
    

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    caption = models.CharField(max_length=255)
    data = models.ImageField(upload_to='photos/')  # Assuming this stores a path or URL to the photo
    tags = models.ManyToManyField(Tag, related_name='photos')

    def __str__(self):
        return self.caption
    
class Comment(models.Model):
    text = models.CharField(max_length=255) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    photo = models.ForeignKey('Photo', on_delete=models.CASCADE, related_name='comments')
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name if self.user else 'Guest'} {self.user.last_name if self.user else ''}: {self.text}"
    
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liked_photos', null=True, blank=True)
    photo = models.ForeignKey('Photo', on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = (('user', 'photo'),)

    def __str__(self):
        return f"Like by {self.user.first_name if self.user else 'Guest'} {self.user.last_name if self.user else ''}"