from django.http import HttpResponse
from django.template import loader, RequestContext
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User


def index(request):
    if request.method == 'GET':
        return HttpResponse('test')


@csrf_protect
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
        #return HttpResponse(loader.get_template('register.html').render())
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']

        if password != password_confirmation:
            return HttpResponse("passwords do not match")

        user = User.objects.create_user('username', 'email@email.email', password)
        user.save()

        return HttpResponse("DONE")
