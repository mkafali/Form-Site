from django.shortcuts import render,redirect
from appforms.models import AppForm
from .models import Answer
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
import json
from datetime import datetime
# Create your views here.
def form_submit(request,form_slug,form_author):
    if request.method == 'POST':
        author_form = User.objects.get(username=form_author)
        if request.user.is_authenticated:
            user = request.user
            #print("mehjwfnfkejcfb")

        else:
            user = User.objects.get(username="anonym")
            #You have to create user anonym first. 

        try:
            form = AppForm.objects.get(author=author_form, slug = form_slug)
            formAuthor = form.author
            formSlug = form.slug
            local_storage_key = f"{user.username}_{formSlug}_{formAuthor}"
            
            if not form.completed:
                if user in form.filled_by.all():
                    for question in form.questions.all():
                        for answer in question.answers.all():
                            if(answer.answered_by == user):
                                answer.delete()
                
                answers = dict()
                for key, value in request.POST.items():
                        if key.startswith('optional_'):
                            answers[key.split("_")[1]] = value

                        elif key.startswith('multi_choices_'):
                            values = request.POST.getlist(key)
                            answers[key.split("_")[2]] = values

                        elif key.startswith('rank_'):
                            answers[key.split("_")[1]] = value
                        
                        elif key.startswith('open_ended_'):
                            answers[key.split("_")[2]] = value

                #print(answers)
                if form.anonymous:
                    for question in form.questions.all():
                        for answer in question.answers.all():
                            if answer.answered_by == user:
                                answer.delete()

                answer_saved = 0
                for question in form.questions.all():
                    answer = answers.get(str(question.number))
                    if answer:
                        answer_saved = Answer.objects.create(question=question,answered_by=user,answer=answer)
                        question.answers.add(answer_saved)
                        if not form.anonymous:
                            form.filled_by.add(user)
                #print("mehmet control")
                

                
                response = redirect('form_page', form_author=form.author, form_slug=form_slug)
                if form.anonymous:
                    cookie_value = answer_saved.answer_slug + "_" + form_slug
                    expire_date = datetime(year=2025, month=5, day=15, hour=1, minute=9, second=15, microsecond=210000)
                    response.set_cookie(local_storage_key, cookie_value, expires=expire_date)
                return response
            
            else:
                messages.error(request,"Form has already completed")
                return redirect('home')
        
        except AppForm.DoesNotExist:
            messages.error(request,"Form Does Not Exist")
            return redirect('home')
        