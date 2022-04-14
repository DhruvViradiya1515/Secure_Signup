from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('signup',views.signup,name='signup'),
    path('Login',views.Login,name='Login'),
    path('signout',views.signout,name='signout'),
    path('contact',views.contact,name='contact'),
    path("about",views.about,name='about'),

    path('activate/<uidb64>/<token>',views.activate,name='activate'),
]