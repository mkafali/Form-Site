from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from users.models import Profile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import QuestionCreate

def create_question(request):
    profile_instance = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = QuestionCreate(request.POST)
        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.author = request.user
            new_question.save()
            return HttpResponse(status=204)
    
    else:
        form = QuestionCreate()

    return render(request, 'create_question.html', {'profile':profile_instance,'form':form})
