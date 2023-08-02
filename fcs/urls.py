# example/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path('', views.index),
    path('cik/<slug:slug>/', views.investor)
]