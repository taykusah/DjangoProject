# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm
from .utils import get_weather_data
from .news_utils import get_news_data
from blog.models import Post

def home(request):
    return render(request, 'core/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.role = 'author'
            user.profile.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Web 2.0 Blog!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})
@login_required
def profile(request):
    return render(request, 'core/profile.html')

def home(request):
    weather_data = get_weather_data('lagos')  # You can pass a city name here
    return render(request, 'core/home.html', {
        'weather_data': weather_data
    })

@login_required
def profile(request):
    weather_data = get_weather_data()
    return render(request, 'core/profile.html', {
        'weather_data': weather_data
    })

def home(request):
    weather_data = get_weather_data()
    news_data = get_news_data()
    recent_posts = Post.objects.filter(status='published').order_by('-created_at')[:5]
    
    return render(request, 'core/home.html', {
        'weather_data': weather_data,
        'news_data': news_data,
        'recent_posts': recent_posts,
    })

@login_required
def profile(request):
    return render(request, 'core/profile.html', {
        'weather_data': get_weather_data(),
    })

# Create your views here.
