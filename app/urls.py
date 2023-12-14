from django.contrib import admin
from django.urls import path
from app import views
from django.views.generic.base import RedirectView

urlpatterns = [

    #This will redirect to the Dashboard if logged in, or to the login page
    path("", RedirectView.as_view(url="/home/")),

    path('home/', views.dashboard, name='dashboard'),
    path('topic/', views.topic),

    path('chart1/', views.chart1),
    path('chart2/', views.chart2),
    path('chart3/', views.chart3),
    path('login/', views.login_view, name= 'login'),
    path('register/', views.register, name= 'register'),
    path('logout/', views.logout_view, name= 'logout'),
    path('contactus/', views.contact, name='contactus'),
    path('aboutus/', views.about_us, name='aboutus'),

]
