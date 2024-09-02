from django.contrib import admin
from django.urls import path
from account.views import *

app_name = 'account'

urlpatterns = [
    
    path('login',login,name="login"),
    path('recover_password',recover_password,name="recover_password"),
    path('register',register,name="register"),
 
]
