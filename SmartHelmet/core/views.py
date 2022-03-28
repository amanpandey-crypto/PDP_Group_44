from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import UserProfile
from django.contrib import messages
# Create your views here.


def home(request):
    return render(request, 'monitor/home.html')


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