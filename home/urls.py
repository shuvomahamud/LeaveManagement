from django.urls import URLPattern, path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("starttime/", views.starttime, name="starttime"),
    path("endtime/", views.endtime, name="endtime"),
    path("completereport/", views.completereport, name="completereport"),
    path("excelreport/", views.excelreport, name="excelreport"),
]