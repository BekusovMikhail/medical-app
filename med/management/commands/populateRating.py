from django.core.management.base import BaseCommand
from med.models import *
import random
import datetime


class Command(BaseCommand):


    def handle(self, *args, **options):
        for doctor in Doctor.objects.all():
            for i in range(random.randint(10, 30)):
                d = datetime.datetime.fromtimestamp(random.randint(1637509068, 1653147468))
                r = Rating(rating=random.randint(1, 5), owner=doctor.user)
                r.save()
                r.creationDate = d
                r.save()

