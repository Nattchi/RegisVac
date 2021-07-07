"""RegisVac URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
(Several lines removed)
"""
from django.contrib import admin
from django.urls import path, include

from main.urls import Home

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('main/', include('main.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]
