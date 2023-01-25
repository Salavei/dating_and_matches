from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from django.contrib.auth.views import LoginView
from django.db.models import Q
from .models import User, Photo, Message, ChatName
from base.utils.business_logic import match_create_user, show_match_people
from .forms import MyUserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from .utils.service import send_register
from django.contrib.auth.mixins import LoginRequiredMixin


class StartPageView(TemplateView):
    template_name = "base/start_page.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_page')
        return super().get(request, *args, **kwargs)


class LoginPageView(LoginView):
    redirect_authenticated_user = True
    template_name = 'base/login.html'

    def get_success_url(self):
        return reverse_lazy('home_page')


class MathPageView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'base/profile.html'

    def get_queryset(self):
        queryset = super(MathPageView, self).get_queryset()
        get_user_queryset = queryset.get(id=self.request.user.id)
        object_list = show_match_people(user=get_user_queryset)
        return object_list


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
                messages.error(request, "You didn't appreciate the pictures!")
            else:
                user.likes = match_create_user(request.POST)
                user.save()
                send_register(email=request.POST.get('email'), password=request.POST.get('password1'))
                login(request, user)
                return redirect('home_page')
        else:
            messages.error(request, 'There was an error during registration!')
    return render(request, 'base/registry.html', context)


@login_required(login_url='login_page')
def chat_page(request, hash):
    to_id = User.objects.get(hash=hash)
    _, _ = ChatName.objects.get_or_create(
        name=request.user.email + to_id.email, user_first=request.user.id, user_second=to_id)
    messages_chat = Message.objects.annotate(queryset1=Q(from_id=request.user.id, to_id=to_id),
                                             queryset2=Q(from_id=request.user.id, to_id=to_id)).select_related(
        'from_id').select_related('to_id').order_by('received_at')
    if request.method == 'POST':
        if request.POST.get('sms'):
            Message.objects.create(from_id=request.user.id, to_id=to_id, message=request.POST.get('sms'))
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
