from pickle import TRUE
from django.db import models

# Create your models here.
class TimeTable(models.Model):
    userid= models.IntegerField()
    startTime = models.DateTimeField(null=True, blank=True)
    endTime = models.DateTimeField(null=True, blank=True)
