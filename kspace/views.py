from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from kspace.models import *


def index(request):
    if request.method == 'GET':
        data = {
            'challenges': Challenge.objects.all()[:4]
        }
        return render(request, 'index.html', data)


def challenge(request, id):
    if request.method == 'GET':
        data = {
            'challenge': Challenge.objects.get(id=id)
        }
        return render(request, 'challenge.html', data)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse('not logged in')
        challenge_name = request.POST['challenge_name']
        challenge_description = request.POST['challenge_discription']
        tags = []
        new_challenge = Challenge(creator=request.user, name=challenge_name, description=challenge_description, tags=tags)
        new_challenge.save()


def challenges(request):
    if request.method == 'GET':
        data = {
            'challenges': Challenge.objects.all()
        }
        return render(request, 'challenges.html', data)


def hall_of_fame(request):
    if request.method == 'GET':
        data = {
            'users': sorted(User.objects.all(), key=lambda x: len(UserChallenge.objects.filter(user=x)), reverse=True)
        }
        return render(request, 'hall_of_fame.html', data)


def profile(request, username=''):
    if request.method == 'GET':
        user = User.objects.get(username=username)
        user_challenges = UserChallenge.objects.filter(user=user)
        data = {
            'user': user,
            'challenges': user_challenges
        }
        return render(request, 'profile.html', data)
