from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import Teacher
from django.utils import timezone
from .tasks import send_new_account_email

def create_teacher_account(request):
    # ... logic kiểm tra quyền admin
    if request.method == 'POST':
        # ... logic lấy thông tin giảng viên từ form
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            user = User.objects.create_user(username=username, email=email, password='ou@123')
            teacher = Teacher.objects.create(user=user, password_reset_time=timezone.now())
            send_new_account_email.delay(user.pk)
            return redirect('admin:accounts_teacher_changelist') # Ví dụ
        except Exception as e:
            # Xử lý lỗi
            print(e)
            return redirect('admin:accounts_teacher_add')
    return redirect('admin:accounts_teacher_add')