"""
URL configuration for tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from trackerapp import views as trackerapp_views
from django.http import HttpResponse
from nutrition import views as nutrition_views
from account import views as account_views
from trackerapp import views
from account import views as account_views

def home(request):
    return HttpResponse("Willkommen auf der Startseite!")

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('account/login/', account_views.login_view, name='login'), 
    path('trackerapp/calendar/', trackerapp_views.calendar_view, name='calendar'),
    path('nutrition/', nutrition_views.search_food, name='nutrition_home'),
    path('nutrition/search-food/', nutrition_views.search_food, name='search_food'),
    path('login/', views.login_view, name='login'),
    path('signup/', account_views.signup_view, name='signup'),
]

