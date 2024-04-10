from django.shortcuts import render,redirect
from appforms.models import AppForm
from django.contrib import messages
from users.models import Profile
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.http import HttpResponse
import json

# Create your views here.

def result_page(request, form_author, form_slug):
    try:
        profile_instance = Profile.objects.get(user=request.user)
        author_user = User.objects.get(username=form_author)
        form = AppForm.objects.get(author=author_user,slug=form_slug)
        return render(request,  'result_page.html' , {'profile':profile_instance,'form':form})

    except AppForm.DoesNotExist:
        messages.error("Form Does Not Exist")
        return redirect('home')
    
def get_answers(request, form_author, form_slug):
    try:
        profile_instance = Profile.objects.get(user=request.user)
        author_user = User.objects.get(username=form_author)
        form = AppForm.objects.get(author=author_user,slug=form_slug)
        all_answers = []
        not_sorted_questions = [i for i in form.questions.all()]
        sorted_questions = sorted(not_sorted_questions, key=lambda x: x.number)
        for question in sorted_questions:
            answers_of_question = []
            if question.type == "OpenEnded":
                answers_of_question.append("false")
            elif question.type == "Rank":
                answers_of_question.append("Rank")
            else:
                answers_of_question.append("true")
            for answer in question.answers.all():
                answers_of_question.append(answer.answer)
                #answers_of_question.append({'answer':answer.answer})
            
            all_answers.append(answers_of_question)

        important_list = []
        for index, answers in enumerate(all_answers):
            if answers[0] == "true" or answers[0] == "Rank":
                question_number = index + 1
                
                if answers[0] == "Rank":
                    important_list.append("Rank")
                else:
                    important_list.append("none")
                
                important_list.append(question_number)
                question = form.questions.get(number=question_number)
                options = question.options.split(",")
                #print(options)
                option_numbers = [str(i) for i in range(1,len(options)+1)]
                results_dict = dict()
                if question.type == "Optional":
                    for index, i in enumerate(option_numbers):
                        frequency = 0
                        for q in answers:
                            if q == i:
                                frequency += 1
                        results_dict[options[index]] = frequency
                elif question.type == "MultiChoices":
                    for index, i in enumerate(option_numbers):
                        actual_option = options[index]
                        frequency = 0
                        for q in answers:
                            for z in q:
                                if z == i:
                                    frequency += 1
                        results_dict[actual_option] = frequency
                
                elif question.type == "Rank":
                    constant = len(option_numbers)
                    #print(answers)
                    #print(option_numbers)
                    results_dict = dict()
                    for index, i in enumerate(option_numbers):
                        for q in options:
                            results_dict[q] = 0

                    
                    for i in answers[1::]:
                        i_list = i.split(",")
                        indexx = 0
                        for q in i_list:
                            #print(q)
                            find_index = options[int(q)-1]

                            results_dict[find_index] = results_dict[find_index] + constant-indexx
                            indexx += 1

                    #print(results_dict)
                    



                important_list.append(results_dict)

        return JsonResponse(important_list, safe=False)
        
    except AppForm.DoesNotExist:
        messages.error("Form Does Not Exist")
        return redirect('home')

def get_who_answered(request, form_author, form_slug):
    try:
        profile_instance = Profile.objects.get(user=request.user)
        author_user = User.objects.get(username=form_author)
        form = AppForm.objects.get(author=author_user,slug=form_slug)
        answered_by = [i.username for i in form.filled_by.all()]
        #print(answered_by)
        #for i in form.filled_by.all():
            #print(i)
        return JsonResponse(answered_by,safe=False)

    except AppForm.DoesNotExist:
        messages.error("Form Does Not Exist")
        return redirect('home')
    
def get_user_answer(request, form_author, form_slug, username):
    try:
        profile_instance = Profile.objects.get(user=request.user)
        author_user = User.objects.get(username=form_author)
        answer_user = User.objects.get(username=username)
        form = AppForm.objects.get(author=author_user,slug=form_slug)
        datas = []
        for question in form.questions.all():
            if question.type == "OpenEnded":
                for answer in question.answers.all():
                    if answer.answered_by == answer_user:
                        datas.append(question.number)
                        datas.append(question.question)
                        datas.append(answer.answer)
                        break
            elif question.type == "Optional":
                for answer in question.answers.all():
                    if answer.answered_by == answer_user:
                        datas.append(question.number)
                        datas.append(question.question)
                        #datas.append(answer.answer)
                        #print(answer.answer)
                        datas_options = question.options.split(",")
                        #print("jbakbwejhfbcjhwec wje")
                        #print(datas_options)
                        datas.append(datas_options[int(answer.answer)-1])
                        break

            elif question.type == "MultiChoices":
                for answer in question.answers.all():
                    if answer.answered_by == answer_user:
                        datas.append(question.number)
                        datas.append(question.question)
                        #datas.append(answer.answer)
                        #print(answer.answer)
                        datas_options = question.options.split(",")
                        #print("mmmmmmmmmmmmmmmmmmmmmmmmmmmm")
                        #print(datas_options)
                        chosed = answer.answer
                        #print(chosed)
                        chosed = chosed.replace("[", "").replace("]", "").replace("'", "").replace(" ","")
                        chosed = chosed.split(",")
                        chosed_list = ["multi"]
                        for i in chosed:
                            #print("jncjskd sjch kdcc cadm lwkec wecmşkale")
                            #print(chosed)
                            #print(type(chosed))
                            int_i = int(i)
                            chosed_list.append(datas_options[int_i-1])  
                        #print(chosed_list)
                        chosed_list_json = json.dumps(chosed_list, ensure_ascii=False)
                        datas.append(chosed_list_json)
                        #datas.append(datas_options[int(answer.answer)-1])
                        break
            else:
                for answer in question.answers.all():
                    if answer.answered_by == answer_user:
                        datas.append(question.number)
                        datas.append(question.question)
                        #datas.append(answer.answer)
                        #print(answer.answer)
                        datas_options = question.options.split(",")
                        #print("rankkkkkkk")
                        #print(datas_options)
                        chosed = answer.answer
                        #print(chosed)
                        chosed = chosed.replace("[", "").replace("]", "").replace("'", "").replace(" ","")
                        chosed = chosed.split(",")
                        chosed_list = ["rank"]
                        for i in chosed:
                            #print("jncjskd sjch kdcc cadm lwkec wecmşkale")
                            #print(chosed)
                            #print(type(chosed))
                            int_i = int(i)
                            chosed_list.append(datas_options[int_i-1])  
                        #print(chosed_list)
                        chosed_list_json = json.dumps(chosed_list, ensure_ascii=False)
                        datas.append(chosed_list_json)
                        #datas.append(datas_options[int(answer.answer)-1])
                        break
                    
        
        #print(datas)
        #return HttpResponse(status=204)
        return JsonResponse(datas,safe=False)


    except AppForm.DoesNotExist:
        messages.error("Form Does Not Exist")
        return redirect('home')