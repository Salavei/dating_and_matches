from django.shortcuts import render, redirect
from .models import User, Photo, Message, ChatName
from base.utils.business_logic import match_create_user, show_match_people
from .forms import MyUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from .utils.service import send_register


def start_page(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    context = {}
    return render(request, 'base/start_page.html', context)


@login_required(login_url='login_page')
def logout_page(request):
    logout(request)
    return redirect('start_page')


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'Пользователя не существует')
            return redirect('home_page')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_page')
        else:
            messages.error(request, 'Пользователья не существует или невверный пароль')
    context = {}
    return render(request, 'base/login.html', context)


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    form = MyUserCreationForm()
    ph = Photo.objects.all()
    context = {'form': form, 'ph': ph}
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            if not match_create_user(request.POST):
                messages.error(request, 'Вы не оценили фотографии!')
            else:
                user.likes = match_create_user(request.POST)
                user.save()
                send_register(email=request.POST.get('email'), password=request.POST.get('password1'))
                login(request, user)
                return redirect('home_page')
        else:
            messages.error(request, 'Произошла ошибка при регистрации!')
    return render(request, 'base/registry.html', context)


@login_required(login_url='login_page')
def match_page(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    obj = User.objects.get(id=request.user.id)
    tmp = show_match_people(user=obj)
    return render(request, 'base/profile.html', {'people': tmp})


@login_required(login_url='login_page')
def chat_page(request, hash):

    from_id = User.objects.get(pk=request.user.id)
    to_id = User.objects.get(hash=hash)
    if not (ChatName.objects.filter(user_first=to_id, user_second=from_id) or ChatName.objects.filter(
            user_first=from_id, user_second=to_id)):
        ChatName.objects.create(name=from_id.email + to_id.email, user_first=from_id, user_second=to_id)
    queryset1 = Message.objects.filter(from_id=from_id, to_id=to_id)
    queryset2 = Message.objects.filter(from_id=to_id, to_id=from_id)
    messages_chat = queryset1.union(queryset2).order_by('received_at')
    if request.method == 'POST':
        if request.POST.get('sms'):
            Message.objects.create(from_id=from_id, to_id=to_id, message=request.POST.get('sms'))
    context = {"messages_chat": messages_chat, 'to_id': to_id}
    return render(request, 'base/chat.html', context)


@login_required(login_url='login_page')
def user_profile(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        if request.POST.get(str(request.user)) == str(request.user):
            request.user.delete()
            return redirect('login_page')
        else:
            form = UserForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
            return redirect('/match/')
    context = {'form': form}
    return render(request, 'base/user_profile.html', context)
