from pyexpat import model
from tabnanny import verbose
from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField


class User(AbstractUser):
    # first_name, last_name
    username = None
    is_patient = models.BooleanField(default=False)
    is_clinic = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default_avatar.jpg')
    USERNAME_FIELD = 'email'
    phone = models.CharField(max_length=20)
    REQUIRED_FIELDS = []
    patronymic = models.CharField(max_length=25, null=True, blank=True)


class Patient(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True)


class Clinic(models.Model):
    description = models.TextField(blank=True)
    specialization = models.CharField(max_length=200, default="")
    address = models.CharField(max_length=75, default="")
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key = True)


class Doctor(models.Model):
    description = models.TextField(blank=True)
    specialization = models.CharField(max_length=50, default="")
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key = True)
    
    class Meta:
        verbose_name = 'Доктор'

class Schedule(models.Model):
    doctor = models.OneToOneField(Doctor, on_delete = models.CASCADE)
    monday = ArrayField(models.TimeField(auto_now=False, auto_now_add=False), size=2, null=True)
    tuesday = ArrayField(models.TimeField(auto_now=False, auto_now_add=False), size=2, null=True)
    wednesday = ArrayField(models.TimeField(auto_now=False, auto_now_add=False), size=2, null=True)
    thursday = ArrayField(models.TimeField(auto_now=False, auto_now_add=False), size=2, null=True)
    friday = ArrayField(models.TimeField(auto_now=False, auto_now_add=False), size=2, null=True)
    saturday = ArrayField(models.TimeField(auto_now=False, auto_now_add=False), size=2, null=True)
    sunday = ArrayField(models.TimeField(auto_now=False, auto_now_add=False), size=2, null=True)



class Chat(models.Model):
    users = models.ManyToManyField(User)
    creationDate = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete = models.CASCADE)
    text = models.TextField()
    sender = models.IntegerField()
    creationDate = models.DateTimeField(auto_now_add=True)


class Event(models.Model):
    # 0 - default, 1 - прием таблеток, 2 - прием у врача, 3 - процедура, 4 - иные события
    type = models.CharField(default='', max_length=50)
    date_time = models.DateTimeField()
    users = models.ManyToManyField(User)
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=500, blank=True)
    instructions = models.CharField(max_length=1000, blank=True)


class Notification(models.Model):
    name = models.CharField(max_length=20)
    sender = models.ForeignKey(User, on_delete = models.CASCADE, related_name='sender', null=True, default=None)
    text = models.TextField()
    creationDate = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None, null=True)

class Procedure(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(default=None, null=True)
    steps = models.TextField(default=None, null=True)
    doctor_spec = models.CharField(max_length=50, default="") # doctors specialization

