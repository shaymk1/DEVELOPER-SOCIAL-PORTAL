from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from . models import *
# from .models import Profile, Message
from . forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import searchProfiles, paginateProfiles


# Create your views here.


def login_user(request):
    page = 'login'
    form = ProfileForm()
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        # email = request.POST['email']
        password = request.POST['password']

        try:

            # checking if the username exist
            # email = User.objects.get(email=email)
            user = User.objects.get(username=username)
        except:

            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username,
                            password=password)  # check if they match

        if user is not None:
            # if user exist, log them in/create a session in the coockie for the user
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
            # return redirect('profiles')

        else:

            messages.error(request, 'Username or Password incorrect')
    context = {

        'page': page,
        'form': form
    }
    return render(request, "users/login_register.html", context)


def logout_user(request):
    logout(request)
    messages.error(request, 'User was logged out successfully!')
    return redirect('login')


def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # dont save it yet,we still wana process it
            user = form.save(commit=False)
            user.username = user.username.lower()  # lower cases
            user.save()

            messages.success(request, 'user account created')

            login(request, user)
            return redirect('edit_account')

        else:
            messages.error(request, 'Error in registering the user!')
    context = {


        'form': form,
        'page': page
    }
    return render(request, "users/login_register.html", context)


def profiles(request):
    profiles, search_query = searchProfiles(request)

    custom_range, profiles = paginateProfiles(request, profiles, 3)
    context = {

        'profiles': profiles,
        'search_query': search_query,
        'custom_range': custom_range

    }
    return render(request, 'users/profiles.html', context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    # skill_set comes from a Profile being the  parent and skill being the child.
    top_skills = profile.skill_set.exclude(description__exact="")
    other_skills = profile.skill_set.exclude(description="")
    context = {

        'profile': profile,
        'top_skills': top_skills,
        'other_skills': other_skills
    }
    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def user_account(request):
    profile = request.user.profile  # this get us the logged in user
    projects = profile.project_set.all()
    # skill_set comes from a Profile being the  parent and skill being the child.
    skills = profile.skill_set.all()

    context = {

        'profile': profile,
        'skills': skills,
        'projects': projects

    }
    return render(request, "users/account.html", context)


@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)

        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'skill added successfully!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    # insance= skill, tells us which skill we are editing
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)

        if form.is_valid():

            form.save()
            messages.success(request, 'skill updated successfully!f')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'skill deleted successfully!')
        return redirect('account')
    context = {

        'object': skill
    }
    return render(request, 'delete_template.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    # related name on recipient is messages
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests,
               'unreadCount': unreadCount
               }
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def view_message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def create_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was successfully sent!')
            return redirect('user_profile', pk=recipient.id)

    context = {
        'recipient': recipient,
        'form': form
    }
    return render(request, 'users/message_form.html', context)
