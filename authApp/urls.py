from django.urls import path 
from authApp import views

app_name = 'authApp'

urlpatterns = [
    path('register/',views.register,name='register'),
    path('index/',views.index,name='index'),
    path('user_login/',views.user_login , name = 'user_login'),
    
    
]