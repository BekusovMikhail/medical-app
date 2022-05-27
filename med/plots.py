from .models import *
import datetime
import plotly
import plotly.express as px
import random
import datetime
import numpy as np


def populate_rating():
    for doctor in Doctor.objects.all():
        for i in range(random.randint(100, 200)):
            d = datetime.datetime.fromtimestamp(random.randint(1637509068, 1653147468))
            r = Rating(rating=random.randint(1,5), rater=Patient.objects.all()[0].user, owner=doctor.user)
            r.save()
            r.creationDate = d
            r.save()


def doctor_ratings_plot(user):
    marks = user.received_ratings.order_by("creationDate")
    dates = marks.values_list('creationDate', flat=True)
    nums = marks.values_list('rating', flat=True)
    nums_avg = []
    for i in range(len(nums)):
        nums_avg.append(np.mean(nums[:i+1]))
    l = plotly.graph_objects.Layout(
        xaxis={'fixedrange': True},
        yaxis={'fixedrange': True})
    fig = px.line(x=dates, y=nums_avg,
                 labels={'x': 'Дата', 'y': 'Средняя оценка'}, title='Изменение среднего рейтинга со временем')
    fig.update_layout(l)
    fig.update_layout(yaxis_range=[0,5])
    code = fig.to_html(full_html=False)
    return code


def doctor_ratings_pie(user):
    marks = user.received_ratings.all()
    counts = []
    for i in range(1, 6):
        counts.append(marks.filter(rating=i).count())
    fig = px.pie(values=counts, names=list(map(lambda x: "Оценка {}".format(x), list(range(1, 6)))), title='Распределение оценок от пациентов')
    code = fig.to_html(full_html=False)
    return code


def doctor_treatments_plot(user):
    today = datetime.date.today()
    today = today.replace(day=1)
    delta = datetime.timedelta(days=2)
    counts = []
    months = []
    for i in range(6):
        months.append(today)
        counts.append(user.doctor.treatment_set.filter(creationDate__month=today.month).count())
        today = today - delta
        today = today.replace(day=1)
    counts.reverse()
    months.reverse()
    l = plotly.graph_objects.Layout(
        xaxis={'fixedrange': True},
        yaxis={'fixedrange': True})
    # data = user.doctor.treatment_set.annotate(month=TruncMonth('creationDate')).values('month').annotate(c=Count('id')).order_by()
    fig = px.bar(x=list(map(lambda x: x.strftime("%B %Y"), months)), y=counts,
                 labels={'x': 'Месяц', 'y': 'Количество пациентов'}, title="Количество пациентов по месяцам")
    fig.update_layout(l)
    code = fig.to_html(full_html=False)
    return code


def doctor_procedures_plot(user):
    today = datetime.date.today()
    today = today.replace(day=1)
    delta = datetime.timedelta(days=2)
    counts = []
    months = []
    procs = CurrentProcedure.objects.none()
    treats = user.doctor.treatment_set.all()
    for treat in treats:
        procs |= treat.currentprocedure_set.all()
    for i in range(6):
        months.append(today)
        counts.append(procs.filter(time__month=today.month).count())
        today = today - delta
        today = today.replace(day=1)
    counts.reverse()
    months.reverse()
    l = plotly.graph_objects.Layout(
        xaxis={'fixedrange': True},
        yaxis={'fixedrange': True})
    fig = px.bar(x=list(map(lambda x: x.strftime("%B %Y"), months)), y=counts,
                 labels={'x': 'Месяц', 'y': 'Количество назначенных процедур'}, title='Количество назначенных процедур')
    fig.update_layout(l)
    code = fig.to_html(full_html=False)
    return code


def patient_ratings_pie(user):
    marks = user.sent_ratings.all()
    counts = []
    for i in range(1, 6):
        counts.append(marks.filter(rating=i).count())
    fig = px.pie(values=counts, names=list(map(lambda x: "Оценка {}".format(x), list(range(1, 6)))),
                 title='Доля выставленных оценок')
    code = fig.to_html(full_html=False)
    return code


def patient_treatments_plot(user):
    today = datetime.date.today()
    today = today.replace(day=1)
    delta = datetime.timedelta(days=2)
    counts = []
    months = []
    for i in range(6):
        months.append(today)
        counts.append(user.patient.treatment_set.filter(creationDate__month=today.month).count())
        today = today - delta
        today = today.replace(day=1)
    counts.reverse()
    months.reverse()
    l = plotly.graph_objects.Layout(
        xaxis={'fixedrange': True},
        yaxis={'fixedrange': True})
    fig = px.bar(x=list(map(lambda x: x.strftime("%B %Y"), months)), y=counts,
                 labels={'x': 'Месяц', 'y': 'Количество обращений в клиники'}, title="Количество обращений в клиники")
    fig.update_layout(l)
    code = fig.to_html(full_html=False)
    return code


def patient_procedures_plot(user):
    today = datetime.date.today()
    today = today.replace(day=1)
    delta = datetime.timedelta(days=2)
    counts = []
    months = []
    procs = CurrentProcedure.objects.none()
    treats = user.patient.treatment_set.all()
    for treat in treats:
        procs |= treat.currentprocedure_set.all()
    for i in range(6):
        months.append(today)
        counts.append(procs.filter(time__month=today.month).count())
        today = today - delta
        today = today.replace(day=1)
    counts.reverse()
    months.reverse()
    l = plotly.graph_objects.Layout(
        xaxis={'fixedrange': True},
        yaxis={'fixedrange': True})
    fig = px.bar(x=list(map(lambda x: x.strftime("%B %Y"), months)), y=counts,
                 labels={'x': 'Месяц', 'y': 'Количество проведенных процедур'}, title='Количество проведенных процедур')
    fig.update_layout(l)
    code = fig.to_html(full_html=False)
    return code


def clinic_treatment_plot(user):
    today = datetime.date.today()
    today = today.replace(day=1)
    delta = datetime.timedelta(days=2)
    counts = []
    months = []
    for i in range(6):
        months.append(today)
        counts.append(user.clinic.treatment_set.filter(creationDate__month=today.month).count())
        today = today - delta
        today = today.replace(day=1)
    counts.reverse()
    months.reverse()
    l = plotly.graph_objects.Layout(
        xaxis={'fixedrange': True},
        yaxis={'fixedrange': True})
    fig = px.bar(x=list(map(lambda x: x.strftime("%B %Y"), months)), y=counts,
                 labels={'x': 'Месяц', 'y': 'Количество обращений пациентов'}, title="Количество обращений пациентов")
    fig.update_layout(l)
    code = fig.to_html(full_html=False)
    return code


def clinic_procedures_plot(user):
    today = datetime.date.today()
    today = today.replace(day=1)
    delta = datetime.timedelta(days=2)
    counts = []
    months = []
    procs = CurrentProcedure.objects.none()
    treats = user.clinic.treatment_set.all()
    for treat in treats:
        procs |= treat.currentprocedure_set.all()
    for i in range(6):
        months.append(today)
        counts.append(procs.filter(time__month=today.month).count())
        today = today - delta
        today = today.replace(day=1)
    counts.reverse()
    months.reverse()
    l = plotly.graph_objects.Layout(
        xaxis={'fixedrange': True},
        yaxis={'fixedrange': True})
    fig = px.bar(x=list(map(lambda x: x.strftime("%B %Y"), months)), y=counts,
                 labels={'x': 'Месяц', 'y': 'Количество проведенных процедур'}, title='Количество проведенных процедур')
    fig.update_layout(l)
    code = fig.to_html(full_html=False)
    return code


def clinic_ratings_plot(user):
    docs = user.clinic.doctor_set.all()
    marks = {}
    for doc in docs:
        t = doc.getAverageRating()
        if t in marks:
            marks[t] += 1
        else:
            marks[t] = 1
    marks = sorted(marks.items(), key=lambda x: x[0])
    l = plotly.graph_objects.Layout(
        xaxis={'fixedrange': True},
        yaxis={'fixedrange': True})
    fig = px.bar(x=list(map(lambda x: x[0], marks)), y=list(map(lambda x: x[1], marks)),
                 labels={'x': 'Средняя оценка', 'y': 'Количество'}, title='Число средних оценок докторов клиники')
    fig.update_layout(l)
    code = fig.to_html(full_html=False)
    return code
