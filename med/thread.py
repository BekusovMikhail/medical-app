import threading
import datetime
import time

from .models import *


def run_continuously(interval=10):
    class CreateNotificationsThread(threading.Thread):
        @classmethod
        def run(cls):
            while True:
                try:
                    events = Event.objects.all()
                    for event in events:
                        diff = (event.date_time.timestamp() - datetime.datetime.now(datetime.timezone(offset=datetime.timedelta(hours=3))).timestamp())
                        if 24 * 3600 - interval < diff <= 24 * 3600 or 3600 - interval < diff <= 3600:
                            if event.type == '3':
                                for user in event.users.all():
                                    if user.is_clinic:
                                        sender = user
                                for user in event.users.exclude(id=sender.id):
                                    notif = Notification(user=user, text=event.name, name="EventNot", sender=sender, event=event)
                                    notif.save()

                            else:
                                for user in event.users.all():
                                    notif = Notification(user=user, text=event.name, name="EventNot", event=event)
                                    notif.save()

                except:
                    print("error")
                time.sleep(interval)

    continuous_thread = CreateNotificationsThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return
