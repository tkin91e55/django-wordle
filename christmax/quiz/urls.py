"""URL configuration for quiz app."""

from django.urls import path

from . import views

app_name = 'quiz'

urlpatterns = [
]

from django.conf import settings

if settings.DEBUG:
    urlpatterns += [
        path('dev/', views.QuizDevView.as_view(), name='dev'),
    ]
