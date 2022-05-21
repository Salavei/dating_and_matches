from django.shortcuts import render, redirect
from .models import User, Photo, Message
from base.utils.business_logic import match_create_user, show_match_people
from .forms import MyUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserForm
from django.contrib.auth.decorators import login_required


def start_page(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    context = {}
    return render(request, 'start_page.html', context)


@login_required(login_url='login_page')
def logout_page(request):
    logout(request)
    return redirect('start_page')


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'Пользователя не существует')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_page')
        else:
            messages.error(request, 'Пользователья не существует или невверный пароль')
    context = {}
    return render(request, 'login.html', context)


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    form = MyUserCreationForm()
    ph = Photo.objects.all()
    context = {'form': form, 'ph': ph}
    print(request.POST)
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        # if form.is_valid():
            # if send_email(email, send_type='app'):
            #     # Регистрационное письмо успешно отправлено
            #     print('Введите код активации')
            # else:
            # user = form.save(commit=False)
            # user.likes = match_create_user(request.POST)
            # user.save()
            # login(request, user)
            # return redirect('home_page')
        # else:
        #     messages.error(request, 'Произошла ошибка при регистрации')
    return render(request, 'registry.html', context)


@login_required(login_url='login_page')
def match_page(request):
    obj = User.objects.get(id=request.user.id)
    tmp = show_match_people(user=obj)
    return render(request, 'profile.html', {'people': tmp})


@login_required(login_url='login_page')
def chat_page(request, pk):
    from_id = User.objects.get(pk=request.user.id)
    to_id = User.objects.get(pk=pk)
    queryset1 = Message.objects.filter(from_id=from_id, to_id=to_id)
    queryset2 = Message.objects.filter(from_id=to_id, to_id=from_id)
    messages_chat = queryset1.union(queryset2)
    if request.method == 'POST':
        Message.objects.create(from_id=from_id, to_id=to_id, message=request.POST.get('sms'))
    context = {"messages_chat": messages_chat}
    return render(request, 'chat.html', context)


@login_required(login_url='login')
def user_profile(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=user.id)
    context = {'form': form}
    return render(request, 'user_profile.html', context)
