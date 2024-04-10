from django.urls import path
from . import views

urlpatterns = [
    path('result_page/<str:form_author>/<slug:form_slug>/', views.result_page, name='result_page'),
    path('get_answers/<str:form_author>/<slug:form_slug>/', views.get_answers, name="get_answers"),
    path('get_who_answered/<str:form_author>/<slug:form_slug>/', views.get_who_answered, name="get_who_answered"),
    path('get_user_answer/<str:form_author>/<slug:form_slug>/<str:username>/', views.get_user_answer, name='get_user_answers'),
    






]