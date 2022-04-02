from datetime import date
from datetime import datetime, timedelta
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import TimeTable
from django.db.models import Q
from django.contrib.auth.models import User

# Create your views here.

def index(response, id):
    ls= TimeTable.objects.filter(userid= id)
    return render(response, "home/list.html", {"ls": ls})

def home(response):
    current_user = response.user
    ls= TimeTable.objects.filter(userid= current_user.id)
    return render(response, "home/list.html", {"ls": ls, "user": current_user})

def starttime(response):
    current_user = response.user
    ls= TimeTable.objects.filter(userid= current_user.id)
    strtm= TimeTable.objects.filter(userid= current_user.id).filter(startTime__date=date.today())
    if not strtm:
        t= TimeTable(userid=current_user.id, startTime= datetime.now())
        t.save(force_insert=True)
    return redirect("/")

def endtime(response):
    current_user = response.user
    ls= TimeTable.objects.filter(userid= current_user.id)
    TimeTable.objects.filter(userid= current_user.id).filter(startTime__date=date.today()).update(endTime= datetime.now())
    return redirect("/")