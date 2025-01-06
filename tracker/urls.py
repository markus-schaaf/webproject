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
from trackerapp import views
from fitness import views as fitness_views
from progress import views as progress_views


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
    path('trackerapp/water-tracker/', views.water_tracker_view, name='water_tracker'),
    path('trackerapp/delete-food-entry/<int:food_unit_id>/', trackerapp_views.delete_food_entry, name='delete_food_entry'),
    path('api/get_completed_days/', trackerapp_views.get_completed_days, name='get_completed_days'),
    path('get_completed_days/', views.get_completed_days, name='get_completed_days'),




    # Nutrition-Routen
    path('nutrition/', nutrition_views.search_food, name='nutrition_home'),
    path('nutrition/search-food/', nutrition_views.search_food_api, name='search_food'),
    path('nutrition/food-details/', nutrition_views.food_details_api, name='search_food'),
    path('nutrition/recent-units/', nutrition_views.recent_food_units, name='recent_used'),
    path('nutrition/food-unit-details/', nutrition_views.food_unit_details, name='recent_used'),
    path('nutrition/save-food-unit/', nutrition_views.save_food_unit, name='save_unit'),


    path('signup/', account_views.signup_view, name='signup'),
    path('trackerapp/recipes/', trackerapp_views.recipes_view, name='recipes'),
    path('check-username/', trackerapp_views.check_username, name='check_username'),
    path('check-email/', trackerapp_views.check_email, name='check_email'),
    path('logout/', trackerapp_views.logout_view, name='logout'),

    #Rezepte
    path('trackerapp/recipes/high_protein/', views.high_protein, name='high_protein'),
    path('trackerapp/recipes/low_carb/', views.low_carb, name='low_carb'),
    path('trackerapp/recipes/low_fat/', views.low_fat, name='low_fat'),
    path('trackerapp/recipes/calories_100_200/', views.calories_100_200, name='calories_100_200'),
    path('trackerapp/recipes/calories_200_400/', views.calories_200_400, name='calories_200_400'),
    path('trackerapp/recipes/calories_400_600/', views.calories_400_600, name='calories_400_600'),
    path('trackerapp/recipes/calories_600_800/', views.calories_600_800, name='calories_600_800'),
    path('trackerapp/recipes/calories_800_1000/', views.calories_800_1000, name='calories_800_1000'),
    path('trackerapp/recipes/calories_1000_1200/', views.calories_1000_1200, name='calories_1000_1200'),
    path('trackerapp/recipes/calories_1200_1400/', views.calories_1200_1400, name='calories_1200_1400'),
    
    # Fitness-Routen
    path('fitness/workout_overview/', fitness_views.workout_overview, name='workout_overview'),
    path('fitness/new_workout/', fitness_views.new_workout_view, name='new_workout_view'),
    path('fitness/get_workout_classes/', fitness_views.get_workout_classes, name='get_workout_classes'),
    path('fitness/get_workout_types/', fitness_views.get_workout_types, name='get_workout_types'),
    path('fitness/save_workout_unit/', fitness_views.save_workout_unit, name='save_workout_unit'),
    path('delete-workout-unit/<int:workout_unit_id>/', fitness_views.delete_workout_unit, name='delete_workout_unit'),

    #progress
    path('trackerapp/progress/', progress_views.progress_home, name='progress_home'),
    path('trackerapp/progress/predict/', progress_views.predict_progress, name='predict_progress'),

]
