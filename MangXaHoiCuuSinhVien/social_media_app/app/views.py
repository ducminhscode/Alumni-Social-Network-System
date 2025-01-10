from celery.apps.multi import MultiParser
from rest_framework.parsers import MultiPartParser
from django.shortcuts import render
from django.http import HttpResponse
from oauthlib.uri_validate import query
from rest_framework.generics import get_object_or_404
from sqlalchemy.dialects.mssql.information_schema import views
from tutorial.quickstart.serializers import UserSerializer
from yaml import serialize

from . import paginators


def index(request):
    return render(request, template_name='index.html', context={
        'name':'SocialMediaApp'
    })

# Create your views here.

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets, generics, permissions
from .serializers import AlumniSerializer, TeacherSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from .tasks import send_new_account_email
from .models import User, Alumni, Teacher
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet

class UserViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]


class AlumniViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Alumni.objects.all()
    serializer_class = AlumniSerializer
    pagination_class = paginators.AlumniPagination

    def get_queryset(self):
        query = self.queryset
        q=self.request.query_params.get("q")

        if q:
            query = query.filter(subject__icontains=q)

        return query


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_alumni(request):
    serializer = AlumniSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Đăng ký thành công. Vui lòng chờ quản trị viên xác nhận.'}, status=status.HTTP_201_CREATED)
    else:
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PATCH'])
@permission_classes([permissions.IsAdminUser])
def approve_alumni(request, pk):
    try:
        alumni = Alumni.object.get(pk=pk)
        alumni.is_verified = True
        alumni.save()
        return Response({'message': 'Đã cho phép đăng ký đối với người dùng này.'}, status=status.HTTP_200_OK)
    except Alumni.DoesNotExist:
        return Response({'error': 'Đã thực hiện xác nhận với yêu cầu này.'}, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['PATCH'])
# @permission_classes([IsAdminUser])
# def reject_alumni(request, pk):
#     alumni = get_object_or_404(Alumni, pk=pk)
#     if alumni.status != '1':
#         return Response({'error': 'Đã thực hiện xác nhận với yêu cầu này.'}, status=status.HTTP_400_BAD_REQUEST)
#     alumni.status = '3'
#     alumni.save()
#     return Response({'message': 'Đã từ chối đăng ký đối với người dùng này.'}, status=status.HTTP_200_OK)



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
