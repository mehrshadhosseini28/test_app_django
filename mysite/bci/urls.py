from django.urls import path

from . import views

app_name = 'bci'
urlpatterns = [
    path('create_and_start/', views.create_and_start, name='create_and_start'),
    path('check_acc/', views.check_acc, name='check_acc')
]
