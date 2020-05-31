from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from bcrypt import gensalt, hashpw, checkpw

from .forms import LoginForm
from .models import User


def index(request):
    if 'user' not in request.session or not request.session['user']:
        return redirect('login')
    return render(request, 'index.html', {'user' : request.session['user']})


def login(request):
    if 'user' in request.session and request.session['user']:
        return redirect('index')
    wrong = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password'].encode()
            user = User.objects.filter(name_field=username)
            if user.count() == 1:
                hash = user[0].hash_field[2:-1].encode()
                correct = checkpw(password, hash)
                if correct:
                    request.session['user'] = username
                    return redirect('index')
            else:
                wrong = True
    return render(request, 'login.html', {'wrong': wrong})


def register2(request):
    if request.method == 'GET':
        if 'username' in request.GET and 'password' in request.GET:
            username = request.GET['username']
            print('Username:', username)
            password = request.GET['password'].encode()
            print('Password:', password)
            salt = gensalt() # This could be used for a DOS attack
            password = hashpw(password, salt)
            print('Salted Password:', password)
            user = User(name_field=username, hash_field=password)
            user.save()
    return redirect('login')


def register(request):
    if 'user' in request.session and request.session['user']:
        return redirect('index')
    wrong = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password'].encode()
            user = User.objects.filter(name_field=username)
            if user.count() == 0:
                salt = gensalt()  # This could be used for a DOS attack
                password = hashpw(password, salt)
                user = User(name_field=username, hash_field=password)
                user.save()
                return redirect('login')
            else:
                wrong = True
    return render(request, 'register.html', {'wrong': wrong})



@csrf_protect
@require_POST
@never_cache
def logout(request):
    del request.session['user']
    return redirect('login')
