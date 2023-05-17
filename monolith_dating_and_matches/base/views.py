from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from django.contrib.auth.views import LoginView
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
    """
    Represents the view for the start page of the application.
    """
    template_name = "base/start_page.html"

    def get(self, request, *args, **kwargs):
        """
        Overrides the get method to check if the user is authenticated.
        If the user is authenticated, it redirects to the home page.
        If the user is not authenticated, it renders the start page template.
        """
        if request.user.is_authenticated:
            return redirect('home_page')
        return super().get(request, *args, **kwargs)


class LoginPageView(LoginView):
    """
    Represents the view for the login page of the application.
    """
    redirect_authenticated_user = True
    template_name = 'base/login.html'

    def get_success_url(self):
        """
        Overrides the get_success_url method to specify the URL to redirect
        after a successful login.
        """
        return reverse_lazy('home_page')


class MathPageView(LoginRequiredMixin, ListView):
    """
    Represents the view for the math page of the application.
    """
    model = User
    template_name = 'base/profile.html'

    def get_queryset(self):
        """
        Overrides the get_queryset method to customize the queryset
        for the math page view.
        """
        queryset = super(MathPageView, self).get_queryset()
        get_user_queryset = queryset.get(id=self.request.user.id)
        object_list = show_match_people(user=get_user_queryset)
        return object_list


def register_page(request):
    """
    Represents the view for the registration page of the application.
    """
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
    """
    Represents the view for the chat page of the application.
    """
    to_id = User.objects.get(hash=hash)
    _, _ = ChatName.objects.get_or_create(
        name=request.user.email + to_id.email, user_first=request.user, user_second=to_id)
    queryset1 = Message.objects.select_related('from_id', 'to_id').filter(from_id=request.user.id, to_id=to_id)
    queryset2 = Message.objects.select_related('from_id', 'to_id').filter(from_id=to_id, to_id=request.user.id)
    messages_chat = queryset1.union(queryset2).order_by('received_at')
    if request.method == 'POST':
        if request.POST.get('sms'):
            Message.objects.select_related('from_id', 'to_id').create(from_id=request.user.id, to_id=to_id,
                                                                      message=request.POST.get('sms'))
    context = {"messages_chat": messages_chat, 'to_id': to_id}
    return render(request, 'base/chat.html', context)


@login_required(login_url='login_page')
def user_profile(request):
    """
    Represents the view for the user profile page of the application.
    """
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
