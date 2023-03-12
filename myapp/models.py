from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

class CustomUser(AbstractUser):
    first_name = None
    last_name = None

    psname = models.CharField(max_length=255, null=True, blank=True)
    pschache = models.CharField(max_length=255, null=True, blank=True)
    casechache = models.CharField(max_length=255, null=True, blank=True)

class PmList(models.Model):
    pmNo = models.IntegerField(default=0)
    pmdate = models.DateField(default=datetime.date.today)
    uniquepmid = models.CharField(max_length=16, unique=True)
    hospitalName = models.CharField(max_length=256)
    doctorName = models.CharField(max_length=256, null=True, blank=True)
    victimName = models.CharField(max_length=256)
    referencePS = models.CharField(max_length=32)
    referenceType = models.CharField(max_length=64)
    referenceNo = models.IntegerField(default=0)
    referenceDate = models.DateField(default=datetime.date.today)
    referenceSection = models.CharField(max_length=256, null=True, blank=True)
    reminderNo = models.IntegerField(default=0)
    lastMemoNo = models.IntegerField(default=0)
    lastMemoDate = models.DateField(default=datetime.date.today)
    status = models.CharField(max_length=64, default='pending')
    investofficer = models.CharField(max_length=256)
    caringcong = models.CharField(max_length=256)
    pmavailablity = models.CharField(max_length=16)
    pmstatus = models.CharField(max_length=16)
    dnaavailablity = models.CharField(max_length=16)
    dnastatus = models.CharField(max_length=16)
    maavailablity = models.CharField(max_length=16)
    mastatus = models.CharField(max_length=16)
    caavailablity = models.CharField(max_length=16)
    castatus = models.CharField(max_length=16)
    otheravailablity = models.CharField(max_length=16)
    otherstatus = models.CharField(max_length=16)

class PmReport(models.Model):
    pmReportDate = models.DateField(auto_now_add=True)
    pmReport = models.TextField()

class ChalanReport(models.Model):
    chalanReportDate = models.DateField(auto_now_add=True)
    chalanReport = models.TextField()
