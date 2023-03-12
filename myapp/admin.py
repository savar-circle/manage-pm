from django.contrib import admin
from .models import CustomUser, PmList, PmReport, ChalanReport

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(PmList)
admin.site.register(PmReport)
admin.site.register(ChalanReport)