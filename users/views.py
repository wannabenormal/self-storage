
from django.db.utils import IntegrityError

from users.models import User

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from .forms import UserCreationForm


def signin(request):
    try:
        if request.method == 'POST':
            user = authenticate(
                email=request.POST['EMAIL'], password=request.POST['PASSWORD']
            )
            login(request, user)
            if user.is_staff:
                return redirect('storages:manager_menu')
            return render(request, 'index.html', context={})

        if request.method == 'GET':
            form = UserCreationForm()
            return render(request, "login.html", context={
                'form': form
            })
    except AttributeError:
        return render(request, "index.html")
    except UnboundLocalError:
        return render(request, "index.html")


def register(request):
    current_site = get_current_site(request)
    context = {}
    try:
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
    except IntegrityError:
        return render(request, 'index.html', context)


def lk(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    user = request.user
    user_boxes = [
        box for order in user.orders.prefetch_related(
            'boxes__storage') for box in order.boxes.all()
    ]
    if request.method == 'POST':
        user.phonenumber = request.POST['PHONE_EDIT']
        user.email = request.POST['EMAIL_EDIT']
        user.save()
    return render(
        request, 'my-rent.html', context={'user_boxes': user_boxes}
    )
