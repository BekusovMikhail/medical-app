import json
from tokenize import triple_quoted
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from regex import E
from .models import *
import datetime
import calendar as calendar_lib


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
    notifications_count = len(user.notification_set.all())
    if user.is_patient:
        role = 'Пациент'
    elif user.is_doctor:
        role = 'Доктор'
    elif user.is_clinic:
        role = 'Клиника'
    else:
        role = "Не определен"

    return render(request, 'med/dashboard.html', context={'role': role, 'name': user.first_name, 'surname': user.last_name, 'notifications_count': notifications_count})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


@login_required
def chats(request):
    user = request.user
    notifications_count = len(user.notification_set.all())
    chats = user.chat_set.all()
    users = User.objects.none()
    for chat in chats:
        users = users.union(chat.users.exclude(id=user.id))
    new_users = User.objects.exclude(id=user.id).exclude(is_staff=True)
    new_users = new_users.difference(users)
    return render(request, 'med/chats.html', context={'users': users, 'new_users': new_users, 'notifications_count': notifications_count})


@login_required
def chat(request):
    id = request.GET['with']
    user1 = request.user
    user2 = User.objects.get(id=id)
    chats1 = user1.chat_set.all()
    chats2 = user2.chat_set.all()
    chat = chats1.intersection(chats2).first()
    notifications_count = len(user1.notification_set.all())
    if chat:
        messages = chat.message_set.all()
        return render(request, 'med/chat.html', {"user1": user1, "user2": user2, "chat": chat, "messages": messages, "ip": "127.0.0.1", 'notifications_count': notifications_count})
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

    return render(request, 'med/calendar.html', context={'days': days, 'next': [y_next, m_next], 'prev': [y_prev, m_prev], 'm_name': m_names[m-1], 'year': y, 'month': m, 'notifications_count': len(user.notification_set.all())})


def create_event(request):
    user = request.user

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

    users = User.objects.exclude(id=user.id).exclude(is_staff=True)
    users_p = Patient.objects.exclude(user_id=user.id)
    users_d = Doctor.objects.exclude(user_id=user.id)
    users_c = Clinic.objects.exclude(user_id=user.id)

    context = {
        'notifications_count': len(user.notification_set.all()),
        'users': users,
        'list_size': min(len(users), 10) + 3,
        'users_p': users_p,
        'users_d': users_d,
        'users_c': users_c,
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
        data.append({'name': 'last_name', 'type': 'text', 'label': 'Фамилия', 'value': request.user.last_name})
        data.append({'name': 'patronymic', 'type': 'text', 'label': 'Отчество', 'value': request.user.patronymic})
        data.append({'name': 'phone', 'type': 'tel', 'label': 'Телефон', 'value': request.user.phone})
        if request.user.is_patient:
            pass
        elif request.user.is_clinic:
            data.append({'name': 'specialization', 'type': 'text', 'label': 'Специализация',
                         'value': request.user.clinic.specialization})
            data.append({'name': 'address', 'type': 'text', 'label': 'Адрес', 'value': request.user.clinic.address})
            data.append(
                {'name': 'description', 'type': 'textarea', 'label': 'Описание', 'value': request.user.clinic.extra})
        elif request.user.is_doctor:
            data.append({'name': 'specialization', 'type': 'text', 'label': 'Специализация',
                         'value': request.user.doctor.specialization})
            data.append(
                {'name': 'description', 'type': 'textarea', 'label': 'Описание', 'value': request.user.doctor.extra})
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
    # if request.method == "POST":
    #     img = request.FILES.get('img', None)
    #     snp = request.POST['fullname']
    #     descr = request.POST.get('description', 'Нет дополнительной информации')
    #     new_phone = request.POST['newphone']
    #     new_email = request.POST['newemail']
    #
    #     usr.user.avatar = img
    #
    #     newname = snp.split()
    #     usr.user.first_name = newname[1]
    #     usr.user.last_name = newname[0]
    #     usr.user.patronymic = newname[2]
    #
    #     usr.extra = descr
    #     usr.user.phone = new_phone
    #
    #     try:
    #         usr.user.email = new_email
    #         usr.save()
    #         usr.user.save()
    #     except:
    #         error = 'Пользователь с такой почтой уже существует'

    fullname = " ".join([usr.user.last_name, usr.user.first_name, usr.user.patronymic])
    
    context = {
        'data': data,
        'usr': usr,
        'fullname': fullname,
        'error': error if error else None,
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

    return render(request, 'med/settings.html', context={'data': context})


def profile(request):
    if 'id' in request.GET:
        user = User.objects.get(id=request.GET['id'])
    elif request.user.is_authenticated:
        user = request.user
    else:
        return HttpResponseForbidden("Forbidden")

    context = {'avatar': user.avatar.url}

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

            treatment.save()

            return HttpResponseRedirect("/dashboard")

        context = {
            'clinics': Clinic.objects.all(),
            'doctors': Doctor.objects.all(),
            }

        return render(request, 'med/create_treatment.html', context=context)
        
    else:
        return HttpResponseRedirect("/dashboard")


@login_required
def accept_treatment(request):
    if request.user.is_clinic:
        context = {}
        print(request.user.id)
        treatments_for_accept = Treatment.objects.filter(status=-1, clinic = request.user.id)
        context_treatments = []
        for treatment in treatments_for_accept:
            tr = {}
            tr['id'] = treatment.id
            tr['patientName'] = Patient.objects.get(pk=treatment.patient).user.first_name + " " + Patient.objects.get(pk=treatment.patient).user.last_name
            tr['doctorName'] = Doctor.objects.get(pk=treatment.doctor).user.first_name + " " + Doctor.objects.get(pk=treatment.doctor).user.last_name
            tr['complaint'] = treatment.complaint
            tr['symptoms'] = treatment.symptoms
            context_treatments.append(tr)
        print(treatments_for_accept)
        return render(request, 'med/accept_treatment.html', context={
            'treatments_for_accept': context_treatments,
        })
        
    else:
        return HttpResponseRedirect("/dashboard")
