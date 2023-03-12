from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard),
    path('home/', views.dashboard, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    path('insertnewpm/', views.insertnewpm, name='insertnewpm'),
    path('edit/<int:id>', views.editpm),
    path('close/<int:id>', views.ClosePM),
    path('archive/', views.Archive, name='archive'),
    path('generateChalan/', views.GeneratePMChalan, name='generateChalan'),
    path('generateReport/', views.GeneratePMReport, name='generateReport'),
    path('viewReport/<str:tbl>/<int:id>', views.ViewReport),
]
