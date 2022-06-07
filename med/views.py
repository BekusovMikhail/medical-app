import json
import os
from tokenize import triple_quoted
from django.conf import settings as sttgs
from django.db.models import Count
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from regex import E
from . import plots
from .models import *
import datetime
import calendar as calendar_lib
import plotly.express as px
from django.db.models.functions import TruncMonth
from numpy import mean

def index(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("dashboard")
        else:
            return HttpResponseForbidden("Forbidden")
    elif request.user.is_authenticated:
        return HttpResponseRedirect("dashboard")
    else:
        return render(request, 'med/index.html')


def reg(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("dashboard")
    else:
        return render(request, 'med/reg.html')


@login_required
def dash(request):
    user = request.user
    plots_list = []
    if user.is_patient:
        role = 'Пациент'
        plots_list.append(plots.patient_ratings_pie(user))
        plots_list.append(plots.patient_procedures_plot(user))
        plots_list.append(plots.patient_treatments_plot(user))
    elif user.is_doctor:
        role = 'Доктор'
        plots_list.append(plots.doctor_treatments_plot(user))
        _ = plots.doctor_ratings_plot(user)
        if _:
            plots_list.append(plots.doctor_ratings_plot(user))
        plots_list.append(plots.doctor_ratings_pie(user))
        plots_list.append(plots.doctor_procedures_plot(user))
    elif user.is_clinic:
        role = 'Клиника'
        plots_list.append(plots.clinic_ratings_plot(user))
        plots_list.append(plots.clinic_treatment_plot(user))
        plots_list.append(plots.clinic_procedures_plot(user))
    else:
        role = "Не определен"

    return render(request, 'med/dashboard.html', context={'role': role, 'name': user.first_name, 'surname': user.last_name, 'plots': plots_list})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


@login_required
def chats(request):
    user = request.user
    chats = user.chat_set.all()
    users = User.objects.none()
    for chat in chats:
        users = users.union(chat.users.exclude(id=user.id))
    new_users = User.objects.exclude(id=user.id).exclude(is_staff=True)
    new_users = new_users.difference(users)
    return render(request, 'med/chats.html', context={'users': users, 'new_users': new_users})


@login_required
def chat(request):
    id = request.GET['with']
    user1 = request.user
    user2 = User.objects.get(id=id)
    chats1 = user1.chat_set.all()
    chats2 = user2.chat_set.all()
    chat = chats1.intersection(chats2).first()
    if chat:
        messages = chat.message_set.all()
        return render(request, 'med/chat.html', {"user1": user1, "user2": user2, "chat": chat, "messages": messages, "ip": sttgs.IP})
    else:
        return HttpResponseRedirect("/chats")


@login_required
def notifications(request):
    user = request.user
    notifications = user.notification_set.all()

    return render(request, 'med/notifications.html', context={'notifications': notifications, 'notifications_count': len(notifications)})


@login_required
def calendar(request):

    if 'y' and 'm' in request.GET:
        y = int(request.GET['y'])
        m = int(request.GET['m'])
    else:
        today = datetime.date.today()
        y = today.year
        m = today.month

    user = request.user

    cal = calendar_lib.Calendar()
    dates = list(cal.itermonthdates(y, m))
    days = list(cal.itermonthdays2(y, m))
    days = list(map(list, days))

    for i in range(len(dates)):
        days[i].append(user.event_set.filter(date_time__date=dates[i]).count())

    if m + 1 == 13:
        y_next = y + 1
        m_next = 1
    else:
        y_next = y
        m_next = m + 1

    if m - 1 == 0:
        y_prev = y - 1
        m_prev = 12
    else:
        y_prev = y
        m_prev = m - 1

    m_names = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

    return render(request, 'med/calendar.html', context={'days': days, 'next': [y_next, m_next], 'prev': [y_prev, m_prev], 'm_name': m_names[m-1], 'year': y, 'month': m})


def create_event(request):
    user = request.user
    if not user.is_clinic and not user.is_doctor:
        return HttpResponseForbidden()
    if request.method == "POST":
        name = request.POST['name']
        date_time = request.POST['date_time']
        description = request.POST['description']
        instructions = request.POST['instructions']
        type_ = request.POST['type']
        user_id_list = request.POST.getlist("user_id[]")

        event = Event(name=name, date_time=date_time, description=description, instructions=instructions, type=type_)
        event.save()
        event.users.add(user)
        for i in user_id_list:
            event.users.add(User.objects.get(id=int(i)))
            event.save()
        
        return redirect('calendar')

    users = User.objects.exclude(id=user.id).exclude(is_staff=True)
    # users_p = Treatment.objects.values_list('patient', flat=True).filter(clinic=user.id)
    # users_p = Patient.objects.filter(pk__in=users_p)
    users_d = []
    if user.is_clinic:
        users_d = user.clinic.doctor_set.all()
    elif user.is_doctor:
        in_clinics = user.doctor.clinics.all()
        for cl in in_clinics:
            users_d.append({'name': cl.user.first_name, 'doctors': cl.doctor_set.all().exclude(user=user)})
    context = {
        'notifications_count': len(user.notification_set.all()),
        'users': users,
        'list_size': min(len(users), 10) + 3,
        # 'users_p': users_p,
        'users_d': users_d,
    }
    return render(request, 'med/create_event.html', context)


def account(request):
    data = []
    if 'id' in request.GET:
        user = User.objects.get(id=request.GET['id'])
    elif request.user.is_authenticated:
        user = request.user
        data = []
        data.append({'name': 'first_name', 'type': 'text', 'label': 'Имя', 'value': request.user.first_name})
        if request.user.is_clinic is False:
            data.append({'name': 'last_name', 'type': 'text', 'label': 'Фамилия', 'value': request.user.last_name})
            data.append({'name': 'patronymic', 'type': 'text', 'label': 'Отчество', 'value': request.user.patronymic})
        data.append({'name': 'phone', 'type': 'tel', 'label': 'Телефон', 'value': request.user.phone})
        if request.user.is_patient:
            data.append({'name': 'passport_number', 'type': 'text', 'label': 'Номер паспорта', 'value': request.user.patient.passport_number})
            data.append({'name': 'passport_series', 'type': 'text', 'label': 'Серия паспорта', 'value': request.user.patient.passport_series})
            data.append({'name': 'snils', 'type': 'text', 'label': 'СНИЛС', 'value': request.user.patient.snils})
            data.append({'name': 'age', 'type': 'number', 'label': 'Возраст', 'value': request.user.patient.age})
            data.append({'name': 'allergies', 'type': 'textarea', 'label': 'Аллергические реакции', 'value': request.user.patient.allergies})
            data.append({'name': 'diseases', 'type': 'textarea', 'label': 'Хронические заболевания', 'value': request.user.patient.diseases})
            data.append({'name': 'extra', 'type': 'text', 'label': 'Дополнительная информация', 'value': request.user.patient.extra})
        elif request.user.is_clinic:
            data.append({'name': 'specialization', 'type': 'text', 'label': 'Специализация', 'value': request.user.clinic.specialization})
            data.append({'name': 'address', 'type': 'text', 'label': 'Адрес', 'value': request.user.clinic.address})
            data.append({'name': 'description', 'type': 'textarea', 'label': 'Описание', 'value': request.user.clinic.extra})
            data.append({'name': 'addressLink', 'type': 'url', 'label': 'Ссылка на местоположение', 'value': request.user.clinic.addressLink})
        elif request.user.is_doctor:
            data.append({'name': 'specialization', 'type': 'text', 'label': 'Специализация', 'value': request.user.doctor.specialization})
            data.append({'name': 'description', 'type': 'textarea', 'label': 'Описание', 'value': request.user.doctor.extra})
            data.append({'name': 'license', 'type': 'text', 'label': 'Номер медицинской лицензии', 'value': request.user.doctor.license})
            data.append({'name': 'license_date', 'type': 'datetime-local', 'label': f'Дата окончания действия лицензии {request.user.doctor.license_date}', 'value': ''})
            data.append({'name': 'experience', 'type': 'number', 'label': 'Стаж', 'value': request.user.doctor.experience})
    else:
        return HttpResponseForbidden("Forbidden")
    usr = user
    if usr.is_doctor:
        usr = usr.doctor
    elif usr.is_clinic:
        usr = usr.clinic
    else:
        usr = usr.patient

    error = None
    if usr.user.is_clinic:
        fullname = usr.user.first_name
    else:
        fullname = " ".join([usr.user.last_name, usr.user.first_name, usr.user.patronymic])
    
    context = {
        'data': data,
        'usr': usr,
        'fullname': fullname,
        'error': error if error else None,
        'notifications_count': len(request.user.notification_set.all()),
    }
    return render(request, 'med/account.html', context)


@login_required
def settings(request):
    context = []
    context.append({'name': 'first_name', 'type': 'text', 'label': 'Имя', 'value': request.user.first_name})
    context.append({'name': 'last_name', 'type': 'text', 'label': 'Фамилия', 'value': request.user.last_name})
    context.append({'name': 'patronymic', 'type': 'text', 'label': 'Отчество', 'value': request.user.patronymic})
    context.append({'name': 'phone', 'type': 'tel', 'label': 'Телефон', 'value': request.user.phone})
    if request.user.is_patient:
        pass
    elif request.user.is_clinic:
        context.append({'name': 'specialization', 'type': 'text', 'label': 'Специализация', 'value': request.user.clinic.specialization})
        context.append({'name': 'address', 'type': 'text', 'label': 'Адрес', 'value': request.user.clinic.address})
        context.append({'name': 'description', 'type': 'textarea', 'label': 'Описание', 'value': request.user.clinic.extra})
    elif request.user.is_doctor:
        context.append({'name': 'specialization', 'type': 'text', 'label': 'Специализация', 'value': request.user.doctor.specialization})
        context.append({'name': 'description', 'type': 'textarea', 'label': 'Описание', 'value': request.user.doctor.extra})

    return render(request, 'med/settings.html', context={'data': context, 'notifications_count': len(request.user.notification_set.all())})


def profile(request):
    if 'id' in request.GET:
        user = User.objects.get(id=request.GET['id'])
    elif request.user.is_authenticated:
        user = request.user
    else:
        return HttpResponseForbidden("Forbidden")

    context = {'avatar': user.avatar.url, 'notifications_count': len(request.user.notification_set.all()),}

    if user.is_patient:
        context['name'] = "{} {} {}".format(user.last_name, user.first_name, user.patronymic)
        context['info'] = []

    elif user.is_clinic:
        context['name'] = user.first_name
        context['info'] = []
        context['info'].append({'title': 'Специализация', 'text': user.clinic.specialization})
        context['info'].append({'title': 'Адрес', 'text': user.clinic.address})
        context['info'].append({'title': 'Описание', 'text': user.clinic.extra})

    elif user.is_doctor:
        context['name'] = "{} {} {}".format(user.last_name, user.first_name, user.patronymic)
        context['info'] = []
        context['info'].append({'title': 'Специализация', 'text': user.doctor.specialization})
        context['info'].append({'title': 'Описание', 'text': user.doctor.extra})


    return render(request, 'med/profile.html', context=context)


@login_required
def create_treatment(request):
    if request.user.is_patient:
        if request.method == "POST":
            complaint = request.POST.get('complaint', 'Жалоба пуста')
            doctor = request.POST['doctor_id']
            symptoms = request.POST.get('symptoms', 'Нет симптомов')
            clinic = request.POST['optGroupSelect']

            treatment = Treatment()
            treatment.doctor = Doctor.objects.get(pk=doctor)
            treatment.clinic = Clinic.objects.get(pk=clinic)
            treatment.patient = Patient.objects.get(pk=request.user.id)
            treatment.complaint = complaint
            treatment.symptoms = symptoms
            treatment.status = -1

            treatment.save()

            notif = Notification()
            notif.sender = treatment.patient.user
            notif.user = treatment.clinic.user
            notif.text = 'Отправлена заявка на лечение'
            notif.save()

            return HttpResponseRedirect("/dashboard")

        context = {
            'clinics': Clinic.objects.all(),
            'doctors': Doctor.objects.all(),
            'notifications_count': len(request.user.notification_set.all()),
            }

        return render(request, 'med/create_treatment.html', context=context)
        
    else:
        return HttpResponseRedirect("/dashboard")


@login_required
def accept_treatment(request):
    if request.user.is_clinic:
        context = {}
  
        treatments_for_accept = Treatment.objects.filter(status=-1, clinic=request.user.id)
        context_treatments = []
        for treatment in treatments_for_accept:
            tr = {}
            tr['id'] = treatment.id
            tr['patientName'] = Patient.objects.get(pk=treatment.patient).user.first_name + " " + Patient.objects.get(pk=treatment.patient).user.last_name
            tr['doctorName'] = Doctor.objects.get(pk=treatment.doctor).user.first_name + " " + Doctor.objects.get(pk=treatment.doctor).user.last_name
            tr['complaint'] = treatment.complaint
            tr['symptoms'] = treatment.symptoms
            context_treatments.append(tr)
        
        return render(request, 'med/accept_treatment.html', context={
            'treatments_for_accept': context_treatments,
            'notifications_count': len(request.user.notification_set.all()),
        })
        
    else:
        return HttpResponseRedirect("/dashboard")


@login_required
def user_treatment_panel(request):
    if request.method == "POST":

        procId = request.POST['procId']
        cur_proc = CurrentProcedure.objects.filter(id=procId)[0]

        resultText = request.POST.get('resultText', None)
        if 'resultImage' in request.FILES:
            resultImage = request.FILES['resultImage']
            cur_proc.resultImage = resultImage      
        
        cur_proc.resultText = resultText
        cur_proc.save()
        

    if not ((request.user.is_doctor or request.user.is_patient) and 'id' in request.GET):
        return HttpResponseForbidden("Forbidden")
    
    if request.user.is_doctor:
        objs = request.user.doctor.treatment_set.filter(id=request.GET['id'])
    if request.user.is_patient:
        objs = request.user.patient.treatment_set.filter(id=request.GET['id'])
    if len(objs) == 0:
        return HttpResponseForbidden("Forbidden")
    treat = objs[0]
    try:
        rating = treat.rating.rating
    except:
        rating = None
    curr_procs = treat.currentprocedure_set.all().order_by('id')
    procs = Procedure.objects.all()
    return render(request, 'med/user_treatment_panel.html', context={'treatment': treat, 'curr_procs': curr_procs, 'procs': procs, 'user':request.user, 'rating': rating})

@login_required
def my_patients(request):
    if not request.user.is_doctor:
        return HttpResponseForbidden()

    treats = Treatment.objects.filter(doctor=request.user.id)
    
    # for patient in Patient.objects.filter(pk__in=patients):
    context = {
        'treats': treats,
    }
    return render(request, 'med/my_patients.html', context)


@login_required
def my_treatments(request):
    if not request.user.is_patient:
        return HttpResponseForbidden()
    treats = Treatment.objects.filter(patient=request.user.id)
    
    # for patient in Patient.objects.filter(pk__in=patients):
    context = {
        'treats': treats,
    }
    return render(request, 'med/my_treatments.html', context)



def search(request):
    clinics = Clinic.objects.all()
    specs = set(Doctor.objects.values_list('specialization', flat=True))
    
    return render(request, 'med/search.html', context={'clinics': clinics, 'specs': specs})