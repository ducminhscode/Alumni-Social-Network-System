from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('teachers/', views.create_teacher_account, name='create_teacher_account'),
]