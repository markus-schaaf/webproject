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
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from trackerapp import views as trackerapp_views
from nutrition import views as nutrition_views
from account import views as account_views
from django.contrib.auth.views import LoginView
from fitness import views as fitness_views

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
    
    # Account-Routen
    path('account/login/', account_views.login_view, name='login'),
    path('signup/', account_views.signup_view, name='signup'),
    path('trackerapp/recipes/', trackerapp_views.recipes_view, name='recipes'),
    path('account/login/', LoginView.as_view(), name='login'),
    
    # TrackerApp-Routen
    path('trackerapp/', trackerapp_views.trackerapp, name='trackerapp'),
    path('trackerapp/calendar/', trackerapp_views.calendar_view, name='calendar'),
    path('trackerapp/fasting/', trackerapp_views.fasting_view, name='fasting'),
    path('trackerapp/account/', trackerapp_views.user_profile_view, name='account'),
    path('trackerapp/edit-profile/', trackerapp_views.edit_profile, name='edit_profile'),

    # Nutrition-Routen
    path('trackerapp/calories/', trackerapp_views.calories_view, name='calories'),
    path('nutrition/', nutrition_views.search_food, name='nutrition_home'),
    path('nutrition/search-food/', nutrition_views.search_food, name='search_food'),


    path('signup/', account_views.signup_view, name='signup'),
    path('trackerapp/recipes/', trackerapp_views.recipes_view, name='recipes'),
    path('check-username/', trackerapp_views.check_username, name='check_username'),
    path('check-email/', trackerapp_views.check_email, name='check_email'),
    path('logout/', trackerapp_views.logout_view, name='logout'),

    path('trackerapp/recipes/', trackerapp_views.recipes_view, name='recipes'),
    path('nutrition/', nutrition_views.search_food, name='search_food'),
    #path('nutrition/search_food/', nutrition_views.search_food_api, name='search_food_api'),
    #path('nutrition/food-details/', nutrition_views.food_details_api, name='food_details_api'),
    #path('nutrition/recent-units/', nutrition_views.recent_food_units, name='recent_food_units'),
    #path('nutrition/food-unit-details/', nutrition_views.food_unit_details, name='food_unit_details'), # für recent used calls

    # Fitness-Routen
    path('fitness/exercise_overview/', fitness_views.exercise_overview_view, name='exercise_overview'),
    path('fitness/new_exercise/', fitness_views.new_exercise_view, name='new_exercise'),
    path('fitness/workout_type_options/', trackerapp_views.workout_type_options, name='workout_type_options'),
    #path('fitness/save_exercise/', trackerapp_views.save_exercise_view, name='save_exercise')
    
    ]


