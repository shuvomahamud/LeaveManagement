from atexit import register
from datetime import date
import time
from datetime import datetime, timedelta
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import TimeTable
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django_user_agents.utils import get_user_agent
from django.http import FileResponse
import pytz
import io
import xlsxwriter

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
            usrTime= TimeTable.objects.filter(userid= usr.id).filter(startTime__date=date.today())
            for singleTime in usrTime:
                singleTime.name= usr.first_name +" "+ usr.last_name
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

@login_required(login_url='/login/')
def completereport(response):
    current_user = response.user
    if current_user.is_superuser:
        usrTimeList= []
        allUser= User.objects.all();
        for usr in allUser:
            usrTime= TimeTable.objects.filter(userid= usr.id)
            for singleTime in usrTime:
                singleTime.name= usr.first_name +" "+ usr.last_name
            usrTimeList.append(usrTime)
        
    return render(response, "home/admin.html", {"list": usrTimeList, "users": allUser})

def is_dst(dt=None, timezone="UTC"):
    if dt is None:
        dt = datetime.utcnow()
    timezone = pytz.timezone(timezone)
    timezone_aware_date = timezone.localize(dt, is_dst=None)
    return timezone_aware_date.tzinfo._dst.seconds != 0


@login_required(login_url='/login/')
def excelreport(request):
  buffer = io.BytesIO()
  workbook = xlsxwriter.Workbook(buffer)
  worksheet = workbook.add_worksheet()
  worksheet.write('A5:A6', 'Date')
  allUser= User.objects.all();
  today = datetime.today()
  charfrom= 66
  j=0
  char1= ""
  k=8
  for j in range (0,31):
    worksheet.write("A"+ str(k+j)+":A"+str(k+j+1), str(j+1))
  for usr in allUser:
    i=5
    usrTime= TimeTable.objects.filter(userid= usr.id).filter(startTime__month=today.month-1)
    name= usr.first_name +" "+ usr.last_name
    worksheet.write(char1+chr(charfrom) +str(i)+":"+chr(charfrom+3) +str(i), name)
    i= i+1
    worksheet.write(char1+chr(charfrom) +str(i)+":"+chr(charfrom+1) +str(i), "In Time")
    worksheet.write(char1+chr(charfrom+1) +str(i)+":"+chr(charfrom+2) +str(i), "Out Time")
    worksheet.write(char1+chr(charfrom+2) +str(i)+":"+chr(charfrom+3) +str(i), "Hour")
    i= i+1
    for singleTime in usrTime:
        xlhour= 0
        xlminute= 0
        print(singleTime.startTime.dst())
        singleTime.startTime= singleTime.startTime + (datetime.fromtimestamp(0) - datetime.utcfromtimestamp(0))
        
        worksheet.write(char1+chr(charfrom) +str(i+ singleTime.startTime.day)+":"+chr(charfrom+1) +str(i+ singleTime.startTime.day), str(singleTime.startTime.hour + 1)+":"+str(singleTime.startTime.minute))
        if singleTime.endTime is None:
            end_time= 0
        else:
            singleTime.endTime= singleTime.endTime + (datetime.fromtimestamp(0) - datetime.utcfromtimestamp(0))
            worksheet.write(char1+chr(charfrom+1) +str(i+ singleTime.startTime.day)+":"+chr(charfrom+2) +str(i+ singleTime.startTime.day), str(singleTime.endTime.hour + 1)+":"+str(singleTime.endTime.minute))
            diff= singleTime.endTime - singleTime.startTime
            days    = divmod(diff.seconds, 86400)        # Get days (without [0]!)
            hours   = divmod(days[1], 3600)               # Use remainder of days to calc hours
            minutes = divmod(hours[1], 60)
            if hours[0] < 23:
                xlhour= hours[0]
                xlminute= minutes[0]
        if singleTime.userid== 10:
            singleTime.startTime.astimezone().isoformat()
            print(singleTime.startTime)
            print(singleTime.startTime.dst())
            
        worksheet.write(char1+chr(charfrom+2) +str(i+ singleTime.startTime.day)+":"+chr(charfrom+3) +str(i + singleTime.startTime.day), str(xlhour)+":"+str(xlminute))
    charfrom= charfrom+3
    if charfrom+3 >=90:
        charfrom= 65
        char1="A"

  workbook.close()
  buffer.seek(0)
  return FileResponse(buffer, as_attachment=True, filename='report.xlsx')