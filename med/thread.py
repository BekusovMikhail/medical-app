import threading
import datetime
import time

from .models import *

import schedule


def run_continuously(interval=10):
    class CreateNotificationsThread(threading.Thread):
        @classmethod
        def run(cls):
            while True:
                try:
                    events = Event.objects.all()
                    for event in events:
                        diff = (event.date_time.timestamp() - datetime.datetime.now(datetime.timezone(offset=datetime.timedelta(hours=3))).timestamp())
                        if 24 * 3600 - 10 < diff <= 24 * 3600 or 3600 - 10 < diff <= 3600:
                            for user in event.users.all():
                                notif = Notification(user=user, text=event.name, name="EventNot", event=event)
                                notif.save()

                except:
                    pass
                time.sleep(interval)

    continuous_thread = CreateNotificationsThread()
    continuous_thread.start()
    return
