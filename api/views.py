from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from med.models import *
from .chatSockets import socketServer


server = socketServer()

@csrf_exempt
def createChat(request):
    if request.method == "POST":
        chat = Chat()
        chat.save()
        user1 = User.objects.get(id=request.session['user_id'])
        user2 = User.objects.get(id=request.POST['receiver'])
        chat.users.add(user1, user2)
        chat.save()
        return HttpResponse(status=201)
    else:
        return HttpResponseForbidden("Forbidden")

@csrf_exempt
def sendMessage(request):
    if request.method == "POST":
        mes = Message()
        mes.chat = Chat.objects.get(id=request.POST['chatId'])
        mes.text = request.POST['text']
        mes.sender = request.POST['sender']
        mes.save()
        target = mes.chat.users.exclude(id=mes.sender).first()
        server.send_message(target.id, mes.text)
        return HttpResponse(status=201)
    else:
        return HttpResponseForbidden("Forbidden")
