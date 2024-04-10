from django.urls import path
from . import views

urlpatterns = [
        path('form_submit/<slug:form_slug>/<str:form_author>/', views.form_submit, name='form_submit'),

]