from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='loginPage'),
    path('signup/', views.signupPage, name='signupPage'),
]

