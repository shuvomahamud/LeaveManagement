from atexit import register
from datetime import date
from datetime import datetime, timedelta
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import TimeTable
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(response, id):
    ls= TimeTable.objects.filter(userid= id)
    return render(response, "home/list.html", {"ls": ls})

@login_required(login_url='/login/')
def home(response):
    current_user = response.user
    if current_user.is_superuser:
        usrTimeList= []
        allUser= User.objects.all();
        for usr in allUser:
            usrTime= TimeTable.objects.filter(userid= usr.id)
            for singleTime in usrTime:
                singleTime.name= usr.first_name + usr.last_name
                print(singleTime)
            usrTimeList.append(usrTime)
        
        return render(response, "home/admin.html", {"list": usrTimeList, "users": allUser})
    else:
        ls= TimeTable.objects.filter(userid= current_user.id)
        return render(response, "home/list.html", {"ls": ls, "user": current_user})

@login_required(login_url='/login/')
def starttime(response):
    current_user = response.user
    ls= TimeTable.objects.filter(userid= current_user.id)
    strtm= TimeTable.objects.filter(userid= current_user.id).filter(startTime__date=date.today())
    if not strtm:
        t= TimeTable(userid=current_user.id, startTime= datetime.now())
        t.save(force_insert=True)
    return redirect("/")

@login_required(login_url='/login/')
def endtime(response):
    current_user = response.user
    ls= TimeTable.objects.filter(userid= current_user.id)
    TimeTable.objects.filter(userid= current_user.id).filter(startTime__date=date.today()).update(endTime= datetime.now())
    return redirect("/")
