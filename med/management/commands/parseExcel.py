
# settings.configure()
# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# django.setup()


# from . import models
import pandas
from datetime import time
import random

from django.core.management.base import BaseCommand
from django.conf import settings
from med.models import *

class Command(BaseCommand):

    def returnTimes(self, medics=None, dayOnRussian=None, index=0):
        if dayOnRussian and not medics.empty:
            if not pandas.isna(medics.iloc[index][dayOnRussian]):
                _ = medics.iloc[index][dayOnRussian].split('-')
                tmp = [time(int(_[0].split(':')[0]), int(_[0].split(':')[1]), 0), time(int(_[1].split(':')[0]), int(_[1].split(':')[1]), 0)]
                return tmp
            else:
                tmp = [None, None]
                return tmp


    def parseScheduleAndDoctors (self, path=None):
        medics = pandas.read_excel(path)
        print(medics)
        for i in range(len(medics)):
            schedule = Schedule()

            schedule.monday = self.returnTimes(medics, 'Пн', i)
            schedule.tuesday = self.returnTimes(medics, 'Вт', i)
            schedule.wednesday = self.returnTimes(medics, 'Ср', i)
            schedule.thursday = self.returnTimes(medics, 'Чт', i)
            schedule.friday = self.returnTimes(medics, 'Пт', i)
            schedule.saturday = self.returnTimes(medics, 'Сб', i)
            schedule.sunday = self.returnTimes(medics, 'Вс', i)

            medic = Doctor()

            us = User()
            us.first_name = medics.iloc[i]['Имя'].strip()
            us.last_name = medics.iloc[i]['Фамилия'].strip()
            us.patronymic = medics.iloc[i]['Отчество'].strip()
            us.email = medics.iloc[i]['Email'].strip()
            us.phone = medics.iloc[i]['Номер телефона'].strip()
            us.is_doctor = True
            #us.set_password("".join([chr(random.randint(65, 65+25) + int(random.choice([0, 32]))) for _ in range(12)]))
            us.set_password("123")
            us.save()
            medic.user = us

            medic.specialization = medics.iloc[i]['Должность']

            schedule.doctor = medic

            medic.schedule = schedule
            medic.save()

            # Временно!!!
            _ = [random.choice(list(Clinic.objects.all())) for i in range(random.randint(2, 5))]
            for k in range(len(_)):
                medic.clinics.add(_[k])
            medic.save()

            schedule.save()


    def parseClinics(self, path=None):
        clinics = pandas.read_excel(path)
        print(clinics)
        for i in range(len(clinics)):
            clinic = Clinic()
            us = User()
            us.first_name = clinics.iloc[i]['Название клиники']
            us.is_clinic = True

            us.email = clinics.iloc[i]['Email'].strip()
            us.phone = clinics.iloc[i]['Телефон']
            us.set_password(str(clinics.iloc[i]['Пароль']))

            us.save()
            clinic.user = us
            clinic.specialization = clinics.iloc[i]['Специализация']
            clinic.address = clinics.iloc[i]['Адрес']
            clinic.save()

    def parseProcedures(self, path=None):
        procedures = pandas.read_excel(path)
        procedures = procedures[["Название процедуры", "Описание", "Пункты для выполнения перед процедурой", "Ответственный за процедуру врач"]]
        print(procedures)
        for i in range(len(procedures)):
            procedure = Procedure()
            procedure.name = procedures.iloc[i]['Название процедуры']
            procedure.description = procedures.iloc[i]['Описание']
            procedure.steps = procedures.iloc[i]['Пункты для выполнения перед процедурой']
            procedure.doctor_spec = procedures.iloc[i]['Ответственный за процедуру врач']
            procedure.save()
            
        return None

    def handle(self, *args, **options):
        self.parseClinics(r"med/excel_files/Kliniki.xls")
        self.parseScheduleAndDoctors(r"med/excel_files/Vrachi.xls")
        self.parseProcedures(r"med/excel_files/Protsedury.xls")

