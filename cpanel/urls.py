from django.urls import path
from . import views

app_name = 'cpanel'

urlpatterns = [
    path('', views.main, name="main"),
    path('ar/', views.mainRTL, name="mainrtl"),

]
