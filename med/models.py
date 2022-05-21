from pyexpat import model
from tabnanny import verbose
from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField


class User(AbstractUser):
    # first_name, last_name
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default_avatar.jpg')
    username = None
    is_patient = models.BooleanField(default=False)
    is_clinic = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    phone = models.CharField(max_length=20)
    REQUIRED_FIELDS = []
    patronymic = models.CharField(max_length=25, null=True, blank=True)


class Patient(models.Model):
    extra = models.TextField(default="")
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True)


class Clinic(models.Model):
    specialization = models.TextField(default="")
    address = models.CharField(max_length=75, default="")
    extra = models.TextField(default="")
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key = True)


class Doctor(models.Model):
    specialization = models.TextField(default="")
    extra = models.TextField(default="")
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key = True)
    
    clinics = models.ManyToManyField(Clinic)

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
    name = models.CharField(max_length=40, default=None, null=True)
    description = models.TextField(default=None, null=True)
    steps = models.TextField(default=None, null=True)
    doctor_spec = models.CharField(max_length=50, default="") # doctors specialization 

class Treatment(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=True, blank=True, unique=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True, unique=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True, unique=False)
    status = models.IntegerField(default=-1, unique=False)
    complaint = models.TextField(default=None, null=True, unique=False)
    symptoms = models.TextField(default=None, null=True, unique=False)
    creationDate = models.DateTimeField(auto_now_add=True)
    closeDate = models.DateTimeField(null=True, blank=True, default=None)

class CurrentProcedure(models.Model):
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE, null=True, blank=True)
    time = models.DateTimeField(blank=True, null=True)
    treatment = models.ForeignKey(Treatment, on_delete = models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    rating = models.FloatField(default=2.0, unique=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, unique=False, related_name='owner')
    rater = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, unique=False, related_name='rater')
    creationDate = models.DateTimeField(auto_now_add=True)

