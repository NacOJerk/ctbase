from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.http import HttpResponse

from bcrypt import gensalt, hashpw, checkpw

from os import listdir
from os.path import isfile, join

from .forms import LoginForm
from .models import User, Challenge, Category, Score
from .question import question, final, questions

def index(request):
    if 'user' not in request.session or not request.session['user']:
        return redirect('login')
    user = get_object_or_404(User, name_field=request.session['user'])
    answered = []
    scored = 0
    for score in user.score_set.all():
        q = score.challenge_field
        scored += q.score_field
        answered.append(q)
    return render(request, 'index.html', {'user': request.session['user'], 'categories': Category.objects.all(),
                                          'questions': Challenge.objects.all(), 'answered': answered, 'score': scored})


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
                    request.session['user-id'] = user.get().id  # This is going to be unsafe hurray
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
            salt = gensalt()  # This could be used for a DOS attack
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
    if 'user' not in request.session:
        return HttpResponse(status=401)
    del request.session['user']
    if 'user-id' not in request.session:
        return HttpResponse(status=401)
    del request.session['user-id']
    return redirect('login')


def answer(request):
    if request.method != 'POST' or 'user' not in request.session or \
            not request.session['user'] or \
            "id" not in request.POST or \
            "answer" not in request.POST:
        return HttpResponse(status=401)
    if request.POST["id"] not in questions:
        return HttpResponse("0")
    user = get_object_or_404(User, name_field=request.session['user'])
    category, question = request.POST["id"].split('-')
    category = get_object_or_404(Category, title_field=category)
    question = get_object_or_404(Challenge, category_field=category, title_field=question)
    try:
        score = Score.objects.get(user_field=user, challenge_field=question)
        return HttpResponse("3")
    except Score.DoesNotExist:
        pass
    result = questions[request.POST["id"]](request.POST["answer"])
    if result == 1:
        score = Score(user_field=user, challenge_field=question)
        score.save()
    return HttpResponse("%d" % result)


onlyfiles = [f for f in listdir("ctf/questions") if isfile(join("ctf/questions", f))]
for file in onlyfiles:
    if file.endswith(".py"):
        file = file.split(".")[0]
        exec("from .questions import %s" % file)# Security threat

final()
