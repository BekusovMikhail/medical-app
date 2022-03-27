from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from .models import User

def index(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        print(password, email)
        us = User.objects.filter(email=email).first()
        if us and us.password == password:
            request.session['user_id'] = us.id
            return HttpResponseRedirect("dashboard")
        else:
            return HttpResponseForbidden("Forbidden")
    return render(request, 'med/index.html')

def reg(request):
    if request.method == "POST":
        user = User()
        user.name = request.POST['name']
        user.surname = request.POST['surname']
        user.email = request.POST['email']
        user.phone = request.POST['phone']
        user.password = request.POST['password']
        user.save()
        request.session['user_id'] = user.id
        return HttpResponseRedirect("dashboard")
    return render(request, 'med/reg.html')

def dash(request):
    if "user_id" in request.session:
        user = User.objects.get(id=request.session['user_id'])
        return render(request, 'med/dashboard.html', context={'name': user.name, 'surname': user.surname})
    else:
        return render(request, 'med/dashboard.html', context={'name': "anon", 'surname': "anon"})

def logout(request):
    if "user_id" in request.session:
        del request.session['user_id']
    return HttpResponseRedirect("/")

def chats(request):
    if "user_id" in request.session:
        user = User.objects.get(id=request.session['user_id'])
        chats = user.chat_set.all()
        users = User.objects.none()
        for chat in chats:
            users = users.union(chat.users.exclude(id=user.id))
        new_users = User.objects.exclude(id=user.id)
        new_users = new_users.difference(users)
        return render(request, 'med/chats.html', context={'users': users, 'new_users': new_users})
    else:
        return render(request, 'med/index.html')

def chat(request):
    if "user_id" in request.session:
        id = request.GET['with']
        user1 = User.objects.get(id=request.session["user_id"])
        user2 = User.objects.get(id=id)
        chats1 = user1.chat_set.all()
        chats2 = user2.chat_set.all()
        chat = chats1.intersection(chats2).first()
        if chat:
            messages = chat.message_set.all()
            return render(request, 'med/chat.html', {"user1": user1, "user2": user2, "chat": chat, "messages": messages, "ip": "127.0.0.1"})
        else:
            return HttpResponseRedirect("/chats")
    else:
        return render(request, 'med/index.html')

def notifications(request):
    if "user_id" in request.session:
        user = User.objects.get(id=request.session['user_id'])
        notifications = user.notification_set.all()
        # notifications = user.notifications_set.all()
        return render(request, 'med/notifications.html', context={'notifications': notifications})
    else:
        return render(request, 'med/dashboard.html', context={'name': "anon", 'surname': "anon"})