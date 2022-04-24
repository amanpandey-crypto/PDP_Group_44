from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import Data, UserProfile
from django.contrib import messages
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotAllowed, JsonResponse
# Create your views here.


def home(request):
    data = []
    r = requests.get('https://api.thingspeak.com/channels/1713185/fields/1.json?results=', params=request.GET)   
    if r.status_code == 200:
        data = r.json()
        print(data)
        sensor_obj = Data(
            pulse=data['feeds'][0]['field1'],
            pressure=data['feeds'][1]['field1'],
            altitude=data['feeds'][2]['field1'],
            temp=data['feeds'][3]['field1'],
        )
        sensor_obj.save()
        print(sensor_obj)
        sensor = Data.objects.all()
    return render(request, 'monitor/home.html', { "sensor": sensor} )


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


# def receive_sensor_data(request):
#     data = []
#     r = requests.get('https://api.thingspeak.com/channels/1713185/fields/1.json?results=1', params=request.GET)   
#     if r.status_code == 200:
#         data = r.json()
#         sensor_obj = Data(
#             pulse=str(data["field1"]),
#             pressure=str(data["field1"]),
#             altitude=str(data["field1"]),
#             temp=str(data["field1"]),
#         )
#         print(sensor_obj)
#         sensor_obj.save()

#     return HttpResponseNotAllowed()