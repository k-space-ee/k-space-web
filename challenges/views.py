from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')

@csrf_protect
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST['user']
        password = request.POST['pw']
        password_confirmation = request.POST['password_confirmation']

        if len(password) < 8:
            return HttpResponse("password too short")

        if password != password_confirmation:
            return HttpResponse("passwords do not match")

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username, password=password)
            user.save()
        else:
            return HttpResponse("user exist")

        return HttpResponse("User {} created".format(username))


@csrf_protect
def login_view(request):
    if request.method == 'GET':
        auth_user = 'no user'
        if request.user.is_authenticated:
            auth_user = request.user.username
        return render(request, 'login.html', {'auth_user': auth_user})
    elif request.method == 'POST':
        username = request.POST['user']
        password = request.POST['pw']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponse('request suq')
        else:
            return HttpResponse('invalid username or password')


def logout_view(request):
    logout(request)
    return HttpResponse('logged out')


def challenge(request):
    if request.method == 'GET':
        return render(request, 'challenge.html')
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse('not logged in')
        challenge_name = request.POST['challenge_name']
        challenge_description = request.POST['challenge_discription']
        tags = []
        challenge = Challenge(creator=request.user, name=challenge_name, description=challenge_description, tags=tags)
        challenge.save()


def dashboard(request):
    if request.method == 'GET':
        data = {'challenges': Challenge.objects.all()}
        return render(request, 'dashboard.html', data)


def hall_of_fame(request):
    if request.method == 'GET':
        data = {
            'users': User.objects.all()
        }
        return render(request, 'hall_of_fame.html', data)


def profile(request, username):
    if request.method == 'GET':

        return render(request, 'profile.html')
