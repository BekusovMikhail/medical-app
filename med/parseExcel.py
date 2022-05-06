# from django.conf import settings
# settings.configure()
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "med.settings")
# django.setup()



# from models import *
import pandas
from datetime import time





def returnTimes(medics=None, dayOnRussian=None):
    if dayOnRussian and medics:
        for i in range(len(medics)):
            if type(medics.iloc[i][dayOnRussian]) != type(0.1):
                print(medics.iloc[i][dayOnRussian].split('-'))
                _ = medics.iloc[i][dayOnRussian].split('-')
                tmp = [time(int(_[0].split(':')[0]), int(_[0].split(':')[1]), 0), time(int(_[1].split(':')[0]), int(_[1].split(':')[1]), 0)]
                print(tmp)
                return tmp
            else:
                tmp = [None, None]
                print(tmp)
                return tmp


def parseScheduleAndDoctors (path=None):

    medics = pandas.read_excel(path)

    print(medics)
    for i in range(len(medics)):
        schedule = Schedule()

        schedule.monday = returnTimes(medics, 'Пн')
        schedule.tuesday = returnTimes(medics, 'Вт')
        schedule.wednesday = returnTimes(medics, 'Ср')
        schedule.thursday = returnTimes(medics, 'Чт')
        schedule.friday = returnTimes(medics, 'Пт')
        schedule.saturday = returnTimes(medics, 'Сб')
        schedule.sunday = returnTimes(medics, 'Вс')

        medic = Doctor()
        medic.user.name = medics.iloc[i]['Имя']
        medic.user.surname = medics.iloc[i]['Фамилия']
        medic.user.patronymic = medics.iloc[i]['Отчество']
        medic.specialization = medics.iloc[i]['Должность']

        schedule.doctor = medic

        medic.schedule = schedule
        medic.save()
        schedule.save()


def parseClinics(path=None):
    clinics = pandas.read_excel(path)
    print(clinics)
    for i in range(clinics):
        clinic = Clinic()
        clinic.user.name = clinics.iloc[i]['Название клиники']
        clinic.specialization = clinics.iloc[i]['Специализация']
        clinic.address = clinics.iloc[i]['Адрес']
        clinic.save()

# parseScheduleAndDoctors("med\excel_files\Vrachi.xlsx")
# parseClinics("med\excel_files\Kliniki.xlsx")