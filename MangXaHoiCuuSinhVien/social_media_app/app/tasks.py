from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Teacher, User


@shared_task
def lock_expired_teacher_accounts():
    teachers = Teacher.objects.filter(must_change_password=True)
    print(2)
    for teacher in teachers:
        teacher.lock_account()
        print(1)
