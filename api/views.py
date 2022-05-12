from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from med.models import *
from .chatSockets import socketServer
import os
import json
import random
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime


server = socketServer()
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "medapp322@gmail.com"
password = "Qwerty2312"


@login_required
@csrf_exempt
def createChat(request):
    if request.method == "POST":
        chat = Chat()
        chat.save()
        user1 = request.user
        user2 = User.objects.get(id=request.POST['receiver'])
        chat.users.add(user1, user2)
        chat.save()
        return HttpResponse(status=201)
    else:
        return HttpResponseForbidden("Forbidden")


@login_required
@csrf_exempt
def sendMessage(request):
    if request.method == "POST":
        mes = Message()
        mes.chat = Chat.objects.get(id=request.POST['chatId'])
        mes.text = request.POST['text']
        mes.sender = request.POST['sender']
        mes.save()
        target = mes.chat.users.exclude(id=mes.sender).first()
        notification = Notification(user=target, text=mes.text, sender=User.objects.get(id=mes.sender), name="ChatNot")
        notification.save()
        server.send_message(mes.chat.id, target.id, mes.text)
        return HttpResponse(status=201)
    else:
        return HttpResponseForbidden("Forbidden")


@csrf_exempt
def sendVerificationCode(request):
    if request.method == "POST" and request.content_type == 'application/json':
        data = json.loads(request.body)
        email = data['email']
        code = "".join(random.sample([str(i) for i in range(10)], 6))
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            msg = MIMEMultipart("alternative")
            msg["Subject"] = u'MedApp Verification code'
            msg["From"] = u"MedApp"
            part1 = MIMEText(u'Your verification code: {}'.format(code),
                             "plain", "utf-8")
            msg.attach(part1)
            server.sendmail(sender_email, email, msg.as_string())
        return HttpResponse(json.dumps({'code': code}), content_type="application/json")

        # mes = Message()
        # mes.chat = Chat.objects.get(id=request.POST['chatId'])
        # mes.text = request.POST['text']
        # mes.sender = request.POST['sender']
        # mes.save()
        # target = mes.chat.users.exclude(id=mes.sender).first()
        # server.send_message(target.id, mes.text)
        # return HttpResponse(status=201)
    else:
        return HttpResponseForbidden("Forbidden")


@csrf_exempt
def registerUser(request):
    if request.method == "POST":
        user = User()
        user.first_name = request.POST['name']
        user.last_name = request.POST['surname']
        user.patronymic = request.POST['patronymic']
        user.email = request.POST['email']
        user.phone = request.POST['phone']
        # user.username = request.POST['email']
        role = request.POST['role']
        user.set_password(request.POST['password'])
        user.save()
        if role == 'patient':
            user.is_patient = True
            reg_user = Patient(user=user)
        elif role == 'doctor':
            user.is_doctor = True
            specialization = request.POST['specialization']
            reg_user = Doctor(specialization=specialization, user=user)
        elif role == 'clinic':
            user.is_clinic = True
            specialization = request.POST['specialization']
            address = request.POST['address']
            reg_user = Clinic(specialization=specialization, address=address, user=user)
        user.save()
        reg_user.save()
        login(request, user)
        return HttpResponse(status=201)
    else:
        return HttpResponseForbidden("Forbidden")


@login_required
@csrf_exempt
def deleteNotification(request):
    if request.method == "POST":
        data = json.loads(request.body)
        not_id = data['notification_id']
        notif = Notification.objects.get(id=not_id)
        if notif:
            notif.delete()
            return HttpResponse(status=201)
        else:
            return HttpResponseForbidden("Forbidden")
    else:
        return HttpResponseForbidden("Forbidden")


@login_required
@csrf_exempt
def getEvents(request):
    if request.method == "POST":
        data = json.loads(request.body)
        resp = list(request.user.event_set.filter(date_time__date=datetime.date(int(data['year']), int(data['month']), int(data['day']))).values())
        for i in resp:
            i['date_time'] = str(i['date_time'])
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponseForbidden("Forbidden")


@login_required
@csrf_exempt
def changeSettings(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.patronymic = request.POST['patronymic']
        user.phone = request.POST['phone']
        if 'avatar' in request.FILES:
            files = os.listdir(r"./med/media/avatars")
            for file in files:
                if file.startswith("{}avatar".format(user.id)):
                    os.remove(os.path.join(r"./med/media/avatars", file))
                    break
            pic = request.FILES['avatar']
            dot = pic.name.rfind('.')
            pic.name = "{}avatar".format(user.id) + pic.name[dot:]
            user.avatar = pic
        if user.is_patient:
            pass
        elif user.is_clinic:
            user.clinic.specialization = request.POST['specialization']
            user.clinic.address = request.POST['address']
            user.clinic.extra = request.POST['description']
            user.clinic.save()
        elif user.is_doctor:
            user.doctor.specialization = request.POST['specialization']
            user.doctor.extra = request.POST['description']
            user.doctor.save()

        user.save()
        return HttpResponse(status=200)

    else:
        return HttpResponseForbidden("Forbidden")


@login_required
@csrf_exempt
def refreshTreatmentStatus(request):
    if request.user.is_clinic:
        data = json.loads(request.body)
        if 'treatment_id' in data:
            treatment = Treatment.objects.filter(id=data['treatment_id'])
            if treatment:
                treatment = treatment[0]
                if data['status'] == "Confirm":
                    treatment.status = 0
                    treatment.save()
                    chat1 = Chat()
                    chat2 = Chat()
                    chat1.save()
                    chat2.save()
                    chat1.users.add(treatment.patient.user, treatment.clinic.user)
                    chat2.users.add(treatment.patient.user, treatment.doctor.user)
                    chat1.save()
                    chat2.save()

                    notif = Notification()
                    notif.sender = treatment.patient.user
                    notif.user = treatment.clinic.user
                    notif.text = 'Отправлена заявка на лечение'
                    notif.save()

                    return HttpResponse(status=200)
                elif data['status'] =="Decline":

                    treatment.delete()
                    return HttpResponse(status=200)
            else:
                return HttpResponseForbidden("Forbidden")
        else:
            return HttpResponseForbidden("Forbidden")
    else:
        return HttpResponseRedirect("/dashboard")


@login_required
@csrf_exempt
def addCurrProcedure(request):
    if not request.user.is_doctor:
        return HttpResponseForbidden("Forbidden")
    treat = request.user.doctor.treatment_set.filter(id=request.POST['treat_id'])
    if len(treat) == 0:
        return HttpResponseForbidden("Forbidden")
    treat = treat[0]
    if request.POST['proc_id'] == '-1':
        proc = Procedure()
        proc.name = request.POST['name']
        proc.description = request.POST['description']
        proc.steps = request.POST['steps']
        proc.save()
    else:
        proc = Procedure.objects.get(id=request.POST['proc_id'])
    currProc = CurrentProcedure()
    currProc.procedure = proc
    currProc.treatment = treat
    currProc.time = request.POST['date_time']
    currProc.save()

    e = Event()
    e.type = '3'
    e.date_time = currProc.time
    e.users.add(request.user, currProc.treatment.patient.user, currProc.treatment.clinic.user)
    e.name = currProc.procedure.name
    e.description = f'Patient: {currProc.treatment.patient.user.first_name} {currProc.treatment.patient.user.last_name}\nDoctor: {currProc.treatment.doctor.user.first_name} {currProc.treatment.doctor.user.last_name}'
    e.instructions = currProc.procedure.steps
    e.save()

    return HttpResponse(status=200)


@login_required
@csrf_exempt
def closeTreatment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        treat = request.user.doctor.treatment_set.get(id=data['treat_id'])
        treat.delete()
        return HttpResponse(status=200)
    else:
        return HttpResponseForbidden("Forbidden")