from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, template_name='index.html', context={
        'name':'SocialMediaApp'
    })

# Create your views here.

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import AlumniSerializer, TeacherSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from .tasks import send_new_account_email



@api_view(['POST'])
@permission_classes([AllowAny])
def register_alumni(request):
    serializer = AlumniSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Đăng ký thành công. Vui lòng chờ quản trị viên xác nhận.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAdminUser]) # Chỉ admin mới được tạo tài khoản
def create_teacher_account(request):
    serializer = TeacherSerializer(data=request.data)
    if serializer.is_valid():
        teacher = serializer.save()
        user = teacher.user
        user.set_password('ou@123')
        user.save()
        send_new_account_email.delay(user.pk)
        return Response({'message': 'Tạo tài khoản giảng viên thành công.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
