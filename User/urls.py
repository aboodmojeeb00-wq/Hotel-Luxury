from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.registration, name='registration'),
    path('doRegistration/', views.doRegistration, name='doRegistration'),
    path('contact/', views.contact, name='contact'),
]
