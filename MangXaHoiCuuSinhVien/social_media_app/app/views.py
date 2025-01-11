from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from .models import User, Alumni, Teacher
from .perms import AdminPermission, AlumniPermission
from .serializers import UserSerializer, AlumniSerializer, TeacherSerializer
from .paginators import Pagination


def index(request):
    return render(request, template_name='index.html', context={
        'name':'SocialMediaApp'
    })

# Create your views here.

class UserViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    pagination_class = Pagination
    permission_classes = [AdminPermission]




class AlumniViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = Alumni.objects.all()
    serializer_class = AlumniSerializer
    pagination_class = Pagination
    parser_classes = [MultiPartParser, ]

    @action(methods=['get'], url_path='list-alumni', detail=False, permission_classes=[AdminPermission])
    def list_alumni(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['patch'], url_path='approve-alumni', detail=True, permission_classes=[AdminPermission])
    def approve_alumni(self, request, pk=None):
        alumni = get_object_or_404(Alumni, pk=pk)

        if alumni.is_verified:
            return Response({"error": "Tài khoản này đã được duyệt."}, status=status.HTTP_400_BAD_REQUEST)

        alumni.is_verified = True
        alumni.save()

        return Response(
            {"message": "Tài khoản cựu sinh viên đã được duyệt.", "alumni_id": alumni.id},
            status=status.HTTP_200_OK
        )



class TeacherViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    pagination_class = Pagination
    parser_classes = [MultiPartParser, ]
