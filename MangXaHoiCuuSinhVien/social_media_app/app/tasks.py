from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Teacher, User


@shared_task
def lock_expired_teacher_accounts():
    teachers = Teacher.objects.filter(must_change_password=True)
    for teacher in teachers:
        if teacher.password_reset_time:
            time_difference = timezone.now() - teacher.password_reset_time
            if time_difference.total_seconds() > 24 * 3600:
                user = teacher.user
                user.is_active = False
                user.save()

@shared_task
def send_new_account_email(user_pk):
    UserModel = get_user_model()
    user = UserModel.objects.get(pk=user_pk)
    subject = "Thông tin tài khoản mới"
    message = f"Chào {user.username},\n\nTài khoản của bạn đã được tạo.\nUsername: {user.username}\nMật khẩu mặc định: ou@123\nVui lòng đổi mật khẩu trong vòng 24h.\nTrân trọng,\nBan quản trị."
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail( subject, message, email_from, recipient_list )

