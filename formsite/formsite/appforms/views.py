from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from users.models import Profile
from django.contrib.auth.decorators import login_required
from .forms import FormCreate, FormQuestionCreate
from django.http import HttpResponse
from questions.models import Questions
from appforms.models import AppForm
from answers.models import Answer
import json
from datetime import datetime
from django.contrib.auth.models import User 
@login_required
def create_form(request):
    profile_instance = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = FormCreate(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.author = request.user
            new_form.save()
            return HttpResponse(status=204)

    else:
        form = FormCreate()

    return render(request, 'create_form.html', {'profile':profile_instance,'form':form})

@login_required
def formquestion(request):
    profile_instance = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = FormQuestionCreate(request.POST)
        if form.is_valid():

            form_title = form.cleaned_data['form_title']
            is_anonymous = request.POST.get('anonymous')
            ask_code = request.POST.get('ask_code')
            if ask_code == "true":
                ask_code = True
            else:
                ask_code = False
            if(is_anonymous=='anonymous'):
                appform = AppForm.objects.create(author=request.user, title=form_title, anonymous=True, ask_code=ask_code)
            else:
                appform = AppForm.objects.create(author=request.user, title=form_title, anonymous=False, ask_code=ask_code)
            profile_instance.my_forms.add(appform)
            question_list = list()
            for key, value in request.POST.items():
                #print(key)
                #if key.startswith('required'):
                    #print(value)
                if key.startswith('new_question_') and not key.startswith('new_question_type_'):
                    index = key.split('_')[-1]
                    new_question_text = value
                    new_number = request.POST.get(f'new_number_{index}')
                    new_question_type = request.POST.get(f'new_question_type_{index}')
                    is_required = request.POST.get(f'required_{index}')
                    if not new_question_type:
                        new_question_type = 'OpenEnded'

                    # Yeni seçeneklerin sayısını dinamik olarak al
                    new_options = []
                    option_index = 0
                    while f'new_options_{index}_{option_index}' in request.POST:
                        new_options.append(request.POST.get(f'new_options_{index}_{option_index}'))
                        option_index += 1

                    new_options = ','.join(filter(None, new_options))

                    if new_number and new_question_text:
                        if is_required=="required" :
                            question_list.append([new_question_text,new_number,new_question_type,new_options,True]) 
                        else:
                            question_list.append([new_question_text,new_number,new_question_type,new_options,False])
                        
                    elif new_question_text:
                        if is_required=="required" :
                            question_list.append([new_question_text,0,new_question_type,new_options,new_options,True])
                        else:
                            question_list.append([new_question_text,0,new_question_type,new_options,new_options,False])
                        
                        
            question_list = sorted(question_list, key=lambda x: x[1])
            for i in question_list:
                new_question = Questions.objects.create(belongs_to=appform, question=i[0], number=i[1], type=i[2], options=i[3], required=i[4])
                appform.questions.add(new_question)
            return redirect('user_profile')
    else:
        form = FormQuestionCreate()

    return render(request, 'form_question.html', {'profile': profile_instance, 'form': form})


def form_page(request,form_author,form_slug):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = User.objects.get(username="anonym")
   
    try:
        form = AppForm.objects.get(slug=form_slug)
        question_list = [i for i in form.questions.all()]
        my_answers = list()
        if request.user in form.filled_by.all():
            for question in form.questions.all():
                for each_answer in question.answers.all():
                    if each_answer.answered_by == request.user:
                        my_answers.append(question.number)
                        my_answers.append(each_answer.answer)
                        
        my_answers_json = json.dumps(my_answers)
        #print(question_list)
        #print(my_answers)
        question_list = sorted(question_list, key=lambda x: x.number)
        formAuthor = form.author
        formSlug = form.slug
        local_storage_key = f"{user.username}_{formSlug}_{formAuthor}"
        stored_author = request.COOKIES.get(local_storage_key, None)
        isFilled = False
        isAnswered = False
        
        if stored_author:
            #print(f"VARRRR_{user.username}")
            isFilled = True
        if request.user.is_authenticated:
            profile_instance = Profile.objects.get(user=request.user)
            if user in form.filled_by.all():
                isAnswered = True
                    
            return render(request, 'form_page.html', {'profile':profile_instance,'form':form,'questions':question_list,'my_answers':my_answers_json,'isFilled':isFilled,'isAnswered':isAnswered})
        else:
            return render(request, 'form_page.html', {'form':form,'questions':question_list,'my_answers':my_answers_json,'isFilled':isFilled,'isAnswered':isAnswered})

    except AppForm.DoesNotExist:
        messages.error(request,"Form Does Not Exist")
        return redirect('home')
    
    


@login_required        
def form_edit(request,form_author,form_slug):
    profile_instance = Profile.objects.get(user=request.user)
    author_form = User.objects.get(username=form_author)
    if author_form == request.user:
        try:
            form_current = AppForm.objects.get(slug=form_slug,author=author_form)
            if not form_current.completed:
                questions_form_current = [i for i in form_current.questions.all()]
                form_title = form_current.title
                form_ask_code = form_current.ask_code
                form_questions = []
                for question in form_current.questions.all():
                    form_questions.append(question.slug)
                #print(form_questions)
                form_questions_json = json.dumps(form_questions)
                return render(request,'form_edit_page.html',{'profile':profile_instance,'form':form_current,'questions':questions_form_current,'form_questions_json':form_questions_json,'form_ask_code':form_ask_code})
            else:
                messages.error(request,'Form has already completed')
                return redirect('home')
        except AppForm.DoesNotExist:
            messages.error(request,'Form Does Not Exist')
            return redirect('home')
    else:
        messages.error(request,"You Are Unauthorized")
        return redirect('home')

@login_required
def form_edit_submission(request, form_slug, form_author):
    if request.method == 'POST':
        author_form = User.objects.get(username=form_author)
        if request.user == author_form:
            try:
                form_current = AppForm.objects.get(author=request.user, slug=form_slug)
                if not form_current.completed:
                    changed_something = False
                    questions_of_form = [i for i in form_current.questions.all()]
                    sorted_questions = sorted(questions_of_form, key=lambda x: x.number)
                    deleted_questions = []
                    not_deleted_questions = {}
                    post_options = []
                    new_questions = []
                    previous_question_count = len(sorted_questions)
                    if form_current.title != request.POST.get("form_title"):
                        form_current.title = request.POST.get("form_title")
                        changed_something = True
                        form_current.save()
                    form_anonymous = request.POST.get("anonymous")
                    if form_current.anonymous and (form_anonymous=="notanonymous"):
                        changed_something = True
                        form_current.anonymous = False
                        form_current.save()
                    elif(not form_current.anonymous and (form_anonymous=="anonymous")):
                        changed_something = True
                        form_current.anonymous = True
                        form_current.save()
                    
                    form_ask_code = request.POST.get("ask_code")
                    if form_current.ask_code and (form_ask_code!="true"):
                        changed_something = True
                        form_current.ask_code = False
                        form_current.save()
                    elif(not form_current.ask_code and (form_ask_code=="true")):
                        changed_something = True
                        form_current.ask_code = True
                        form_current.save()

                    form_completed = request.POST.get("form_complete")
                    if form_completed == "true":
                        form_current.completed = True
                        form_current.save()

                    

                    for key,value in request.POST.items():
                        #print(key,value)
                        if key.startswith("new_number"):
                            if int(key.split("_")[-1]) <= len(sorted_questions):
                                not_deleted_questions[key.split("_")[-1]] = value
                            else:
                                new_questions.append(key)
                                changed_something = True

                        if key.startswith("new_options"):
                            post_options.append(key)


                    for i in range(1,previous_question_count+1):
                        if not str(i) in not_deleted_questions.keys():
                            deleted_questions.append(i)
                            changed_something = True

                    for i in deleted_questions:
                        question = Questions.objects.get(belongs_to=form_current,number=int(i))
                        form_current.questions.remove(question)
                        question.delete()

                    changed_slugs = set()

                    for i in not_deleted_questions.keys():
                        question_number = not_deleted_questions[i]
                        for question in form_current.questions.all():
                            if question.number == int(i) and not question.slug in changed_slugs:
                                question.number = int(question_number)
                                changed_slugs.add(question.slug)
                                question.save()

                    for key in request.POST.keys():
                        if key.startswith("new_number"):
                            if int(key.split("_")[-1]) > len(sorted_questions):
                                changed_something = True
                                new_options = []
                                key_number = int(key.split("_")[-1])
                                option_index = 0

                                for i in post_options:
                                    if i.startswith(f'new_options_{key_number}'):
                                        if(request.POST.get(i)):
                                            new_options.append(request.POST.get(i))
                                
                                
                                new_options = ','.join(filter(None, new_options))
                                new_question_number = request.POST.get(f"new_number_{key_number}")
                                new_question = request.POST.get(f"new_question_{key_number}")
                                new_type = request.POST.get(f"new_question_type_{key_number}")
                                is_required = request.POST.get(f"required_{key_number}")
                                if is_required == "notrequired":
                                    is_required = False
                                else:
                                    is_required = True
                                if new_type == "OpenEnded" or new_options: 
                                    question_created = Questions.objects.create(belongs_to=form_current, question=new_question, number=new_question_number, type=new_type, options=new_options, required=is_required)
                                else:
                                    question_created = Questions.objects.create(belongs_to=form_current, question=new_question, number=new_question_number, type="OpenEnded", options=new_options, required=is_required)
                                
                                form_current.questions.add(question_created)
                    
                    if changed_something:
                        current_date = datetime.now()
                        if not form_current.is_changed:
                            form_current.is_changed = True
                        form_current.changed_time = str(current_date.date()) + " " + str(current_date.hour) + "." + str(current_date.minute)
                        form_current.save()
                    return redirect('form_page', form_author=request.user.username, form_slug=form_slug)   
                else:
                    messages.error(request,"Form has already completed")
                    return redirect('home')

            except AppForm.DoesNotExist:
                messages.error(request,"Form does not exist")
                return redirect('home')
        else:
            messages.error(request,"You Are Unauthorized")
            return redirect('home')
    