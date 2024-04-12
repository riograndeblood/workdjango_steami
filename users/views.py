from django.shortcuts import render, redirect
import django.db.utils
from django.http import HttpResponse
from .forms import UserForm,LoginUserForm
from django.contrib.auth.models import User
import django
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings


def register_user(request):
    if request.method == "GET":
        form = UserForm()
        return render(request, 'registration/register.html',
                      context={'form' : form})
    else:
        email = request.POST['email']
        if User.objects.filter(email=email).count() != 0:
            return HttpResponse('<h1>Такой пользователь уже существует</h1>')
        else:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                email=request.POST['email'])
            except django.db.utils.IntegrityError:
                return HttpResponse ('<h1>This user exists</h1>')
            user.set_password(request.POST['password'])
            user.save()
            send_mail('Successful registration',
                      'You have successfully registered',
                      settings.DEFAULT_FROM_EMAIL,
                      settings.RECIPIENTS_EMAIL)
            return HttpResponse('<h1>Вы успешно зарегистрировались</h1>')

def login_user(request):
    if request.META.get('HTTP_REFERER') == 'http://127.0.0.1:8000/get_games/':
        redirect_url = ''
    else:
        redirect_url = 'games'
    if request.method == 'GET':
        form = LoginUserForm()
        return render(request,'registration/login.html',
                      context={'form' : form})
    else:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,
                            password=password)
        if user is not None:
            login(request,user=user)
        else:
            return HttpResponse('<h1>Wrong login or password</h1>')
        return redirect(redirect_url)


def logout_user(request):
    if request.user.is_authenticated:
        # if request.environ['HTTP_REFERER'] == 'http://127.0.0.1:8000/get_games/':
        logout(request)
        return redirect('login')







