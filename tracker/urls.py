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
from django.urls import path
from django.http import HttpResponse
from trackerapp import views as trackerapp_views
from nutrition import views as nutrition_views
from account import views as account_views

# Startseite
def home(request):
    return HttpResponse("Willkommen auf der Startseite!")

urlpatterns = [
    # Allgemeine Routen
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    
    # Account-Routen
    path('account/login/', account_views.login_view, name='login'),
    path('account/signup/', account_views.signup_view, name='signup'),

    # TrackerApp-Routen
    path('trackerapp/', trackerapp_views.trackerapp, name='trackerapp'),
    path('trackerapp/calendar/', trackerapp_views.calendar_view, name='calendar'),
    path('trackerapp/fasting/', trackerapp_views.fasting_view, name='fasting'),

    # Nutrition-Routen
    path('nutrition/', nutrition_views.search_food, name='search_food'),
    path('nutrition/search_food/', nutrition_views.search_food_api, name='search_food_api'),
    path('nutrition/food-details/', nutrition_views.food_details_api, name='food_details_api'),
    path('nutrition/recent-units/', nutrition_views.recent_food_units, name='recent_food_units'),
    path('nutrition/food-unit-details/', nutrition_views.food_unit_details, name='food_unit_details'), # für recent used calls
]


