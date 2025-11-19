"""URL configuration for quiz app."""

from django.urls import path

from . import views

app_name = 'quiz'

urlpatterns = [
    path('dev/', views.QuizDevView.as_view(), name='dev'),
]
