from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RideRequestForm
from django.contrib.auth.models import User
from .models import Ride
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.

def home(request):
    return render(request, 'home.html')

@login_required
def request_ride(request):
    if request.method == 'POST':
        form = RideRequestForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.rider = request.user
            ride.save()
            return redirect('home')
    else:
        form = RideRequestForm()
    return render(request, 'request_ride.html', {'form': form})

@login_required
def driver_dashboard(request):
    # Only show unassigned rides
    available_rides = Ride.objects.filter(status='requested', driver__isnull=True)
    return render(request, 'driver_dashboard.html', {'rides': available_rides})

@login_required
def accept_ride(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)
    if ride.status == 'requested' and ride.driver is None:
        ride.driver = request.user
        ride.status = 'accepted'
        ride.save()
    return redirect('driver_dashboard')

@login_required
def rider_history(request):
    rides = Ride.objects.filter(rider=request.user).order_by('-created_at')
    return render(request, 'rider_history.html', {'rides': rides})

@login_required
def driver_active_rides(request):
    rides = Ride.objects.filter(driver=request.user, status='accepted').order_by('-created_at')
    return render(request, 'driver_active_rides.html', {'rides': rides})

@login_required
def complete_ride(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id, driver=request.user)
    if ride.status == 'accepted':
        ride.status = 'completed'
        ride.save()
    return redirect('driver_active_rides')

@login_required
def deny_ride(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id, status='requested')

    # Optional: only allow drivers
    if not request.user.is_staff:
        return redirect('driver_dashboard')

    if request.method == 'POST':
        ride.status = 'denied'
        ride.driver = None
        ride.save()
        messages.success(request, 'Ride has been denied.')
    
    return redirect('driver_dashboard')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after signup
            if user.role == 'driver':
                return redirect('driver_dashboard')  # replace with your actual driver URL
            else:
                return redirect('request_ride')   # replace with your actual rider URL
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == 'driver':
                return redirect('driver_dashboard')
            elif user.role == 'rider':
                return redirect('request_ride')
            else:
                return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def dashboard(request):
    if request.user.role == 'driver':
        return render(request, 'driver_dashboard.html')
    elif request.user.role == 'rider':
        return render(request, 'request_ride.html')
    else:
        return redirect('login')
    

