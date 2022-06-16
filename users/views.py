from users.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def signin(request):
    if request.method == 'POST':
        if 'EMAIL' in request.POST:
            user = authenticate(email=request.POST['EMAIL'], password=request.POST['PASSWORD'])
            login(request, user)
            return render(request, 'index.html',context={})


def register(request):
    context = {}
    if request.method == 'POST':
        email = request.POST['EMAIL_CREATE']
        password = request.POST['PASSWORD_CREATE']
        User.objects._create_user(
                password=password,
                email=email,
                username=email,
        )
        user = authenticate(email=request.POST['EMAIL_CREATE'], password=request.POST['PASSWORD_CREATE'])
        # TODO Добавить уведомление о регистрации на email
        login(request, user)
        return render(request, 'index.html', context)
    if request.method == 'GET':
        return render(request, 'index.html', context)
