from users.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site


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
        return redirect('login')
    if request.method == 'GET':
        return render(request, 'index.html', context)
