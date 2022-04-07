from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import UserProfile
from django.contrib import messages
import requests
# Create your views here.


def home(request):
    data = []
    r = requests.get('https://api.thingspeak.com/channels/1312691/feeds.json?api_key=TINNGV928QN3S2A7&results=1', params=request.GET)   
    if r.status_code == 200:
        data = r.json()
        print(data)
    temp = data['feeds'][0]['field1'] 
    mositure =  data['feeds'][0]['field2']
    at =  data['feeds'][0]['field3']
    ht= data['feeds'][0]['field4']
        
    return render(request, 'monitor/home.html', {'temp': temp, 'mositure': mositure, 'at':  at, 'ht':  ht, 'activedashboard': 'active'})


def register(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)
            objt = UserProfile(user=user, contactno=request.POST.get('ContactNo'), 
                               user_image=request.POST.get('user_image'))

            objt.save()
            return redirect('login')

    context = {'form': form}
    return render(request, 'monitor/signup.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'monitor/login.html', context)


def logoutUser(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out')
    return redirect('login')