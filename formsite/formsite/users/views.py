from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, UserProfileUpdateForm, ProfileEditForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from appforms.models import AppForm
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        try:
            profile_instance = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            Profile.objects.create(user=request.user)
            profile_instance = Profile.objects.get(user=request.user)
        finally:
            return render(request, 'home.html', {'profile':profile_instance})
        
    return render(request, 'home.html', {})


def user_login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, f"Username or Password is wrong")
            return render(request, 'user_login.html', {})

    return render(request, 'user_login.html', {})

def user_logout(request):
    logout(request)
    return redirect('home')

def user_register(request):
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            Profile.objects.create(user=user)
            return redirect('home')
    else:
        form = SignUpForm()


    return render(request, 'register.html', {'form':form})

@login_required
def user_profile(request):
    profile_instance = Profile.objects.get(user=request.user)
    my_forms = profile_instance.my_forms.all()
    return render(request, 'user_profile.html', {'profile':profile_instance,'my_forms':my_forms})

@login_required
def profile_edit(request):
    profile_instance = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile_instance)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = ProfileEditForm(instance=profile_instance)
    return render(request, 'profile_edit.html', {'form':form,'profile':profile_instance})
    
@login_required
def user_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method=='POST':
        form = UserProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_edit')
    else:
        form = UserProfileUpdateForm(instance=request.user)

    return render(request, 'user_edit.html', {'form':form,'profile':profile})

def dark_mode(request):
    if request.method == 'POST':
        profile_instance = Profile.objects.get(user=request.user)
        if profile_instance.dark_mode:
            profile_instance.dark_mode = False
        else:
            profile_instance.dark_mode = True
        profile_instance.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
def search_code(request):
    if request.user.is_authenticated:
        profile_instance = Profile.objects.get(user=request.user)
        if request.method=='POST':
            searched = request.POST.get('searched','')
            if not searched:
                return render(request, 'search.html', {'profile':profile_instance,'form':None})
            else:
                try:
                    searched_form = AppForm.objects.get(form_code=searched)
                    return render(request, 'search.html', {'profile':profile_instance,'form':searched_form})
                except AppForm.DoesNotExist:
                    return render(request, 'search.html', {'profile':profile_instance,'form':None})
        else:
            return HttpResponse(status=204)
    else:
        if request.method=='POST':
            searched = request.POST.get('searched','')
            if not searched:
                return render(request, 'search.html', {'form':None})
            else:
                try:
                    searched_form = AppForm.objects.get(form_code=searched)
                    return render(request, 'search.html', {'form':searched_form})
                except AppForm.DoesNotExist:
                    return render(request, 'search.html', {'form':None})
                

