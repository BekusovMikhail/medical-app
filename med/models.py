from django.contrib.postgres.fields import ArrayField
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

class Notification(models.Model):
    name = models.CharField(max_length=20)
    sender = models.TextField()
    text = models.TextField()
    creationDate = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)


class Chat(models.Model):
    users = models.ManyToManyField(User)
    creationDate = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete = models.CASCADE)
    text = models.TextField()
    sender = models.IntegerField()
    creationDate = models.DateTimeField(auto_now_add=True)

