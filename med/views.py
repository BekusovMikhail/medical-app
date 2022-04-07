from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import *


def index(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            print('dasdas')
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
    return render(request, 'med/dashboard.html', context={'name': user.first_name, 'surname': user.last_name, 'notifications_count': notifications_count})


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

    context = {
        'notifications_count': len(user.notification_set.all()),
        'users': users,
        'list_size': min(len(users), 10) + 3
    }
    return render(request, 'med/create_event.html', context)