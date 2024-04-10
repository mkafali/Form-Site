from django.urls import path
from . import views

urlpatterns = [
    path('create_form/', views.create_form, name='create_form'),
    path('form_question/', views.formquestion, name='form_question'),
    path('form_page/<str:form_author>/<slug:form_slug>/', views.form_page, name='form_page'),
    path('form_edit/<str:form_author>/<slug:form_slug>/', views.form_edit, name='form_edit'),
    path('form_edit_submission/<slug:form_slug>/<str:form_author>/', views.form_edit_submission, name='form_edit_submission'),
    


    

]