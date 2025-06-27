from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('request-ride/', views.request_ride, name='request_ride'),
    path('driver-dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('accept-ride/<int:ride_id>/', views.accept_ride, name='accept_ride'),
    path('rider-history/', views.rider_history, name='rider_history'),
    path('driver-rides/', views.driver_active_rides, name='driver_rides'),
    path('complete-ride/<int:ride_id>/', views.complete_ride, name='complete_ride'),
    path('driver-active-rides/', views.driver_active_rides, name='driver_active_rides'),
    path('deny_ride/<int:ride_id>/', views.deny_ride, name='deny_ride'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

]



