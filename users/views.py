from users.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from .forms import UserCreationForm


def signin(request):
    if request.method == 'POST':
        user = authenticate(
            email=request.POST['EMAIL'], password=request.POST['PASSWORD']
        )
        login(request, user)
        if user.is_staff:
            return redirect('storages:view_orders')
        return render(request, 'index.html', context={})
        
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, "login.html", context={
            'form': form
        })


def register(request):
    current_site = get_current_site(request)
    context = {}
    if request.method == 'POST':
        email = request.POST['EMAIL_CREATE']
        password = request.POST['PASSWORD_CREATE']
        User.objects._create_user(
            password=password,
            email=email,
            username=email,
        )
        subject_message = 'Вы успешно зарегестрированы на SelfStorage'
        message = f'''
            Чтобы войти пройдите по ссылке: http://{current_site.domain}
            Ваш логин: {email}
            Ваш пароль: {password}
            '''
        EmailMessage(
            subject=subject_message,
            body=message,
            to=[email],
        ).send()
        user = authenticate(
            email=request.POST['EMAIL_CREATE'],
            password=request.POST['PASSWORD_CREATE']
        )
        login(request, user)
        return render(request, 'index.html', context)
    if request.method == 'GET':
        return render(request, 'index.html', context)
