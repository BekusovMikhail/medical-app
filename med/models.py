from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    phone = models.CharField(max_length=20)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key = True)


class Clinic(models.Model):
    phone = models.CharField(max_length=20)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key = True)


class Doctor(models.Model):
    phone = models.CharField(max_length=20)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key = True)


class Chat(models.Model):
    users = models.ManyToManyField(User)
    creationDate = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete = models.CASCADE)
    text = models.TextField()
    sender = models.IntegerField()
    creationDate = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    name = models.CharField(max_length=20)
    sender = models.ForeignKey(User, on_delete = models.CASCADE, related_name='sender')
    text = models.TextField()
    creationDate = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
