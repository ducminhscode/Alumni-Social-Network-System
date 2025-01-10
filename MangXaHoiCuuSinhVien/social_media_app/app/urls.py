from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .serializers import UserSerializer
from .views import UserViewSet, AlumniViewSet
from . import views

r = DefaultRouter()
r.register(r'users', UserViewSet, basename='user')
r.register('alumni', AlumniViewSet, basename='alumni')

urlpatterns = [
    path('', include(r.urls)),
    path('teachers/', views.create_teacher_account, name='create_teacher_account'),

    path('register-alumni/', views.register_alumni, name='register_alumni'),
    path('approve-alumni/<int:pk>/', views.approve_alumni, name='approve_alumni'),
]