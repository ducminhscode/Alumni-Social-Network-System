from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now as timezone_now
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from .models import User, Alumni, Teacher
from . import serializers



class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = Alumni.objects.all()
    serializer_class = serializers.AlumniSerializer

    @action(methods=['post'], url_path='register-alumni', detail=False)
    def register_alumni(self, request):
        serializer = serializers.AlumniSerializer(data=request.data)
        if serializer.is_valid():
            # Validate avatar presence
            avatar = serializer.validated_data['user'].get('avatar', None)
            if not avatar:
                return Response({"error": "Avatar is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Save alumni data and deactivate account (admin approval needed)
            alumni = serializer.save()
            alumni.user.is_active = False
            alumni.user.save()

            return Response({"message": "Alumni registered successfully. Pending admin approval."},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(methods=['post'], url_path='login', detail=False, permission_classes=[])
    # def login(self, request):
    #     """
    #     Endpoint for user login.
    #     Validates alumni, teacher, or admin role.
    #     """
    #     username = request.data.get('username')
    #     password = request.data.get('password')
    #
    #     user = authenticate(username=username, password=password)
    #
    #     if not user:
    #         return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)
    #
    #     if not user.is_active:
    #         return Response({"error": "Account is deactivated. Contact admin for support."},
    #                         status=status.HTTP_403_FORBIDDEN)
    #
    #     # Role-based login response
    #     role_mapping = {0: "Admin", 1: "Alumni", 2: "Teacher"}
    #     role = role_mapping.get(user.role, "Unknown")
    #
    #     return Response({"message": f"Logged in as {role}.", "role": role}, status=status.HTTP_200_OK)
    #
    # @action(methods=['post'], url_path='register-teacher', detail=False, permission_classes=[IsAuthenticated])
    # def register_teacher(self, request):
    #     """
    #     Endpoint for admin to create teacher accounts.
    #     Sends default login info via email.
    #     """
    #     if request.user.role != 0:
    #         return Response({"error": "Only admins can create teacher accounts."}, status=status.HTTP_403_FORBIDDEN)
    #
    #     serializer = serializers.TeacherSerializer(data=request.data)
    #     if serializer.is_valid():
    #         teacher = serializer.save()
    #         teacher.user.set_password('ou@123')  # Default password
    #         teacher.user.is_active = True
    #         teacher.user.save()
    #
    #         # Send email to the teacher with login credentials
    #         send_mail(
    #             subject="Teacher Account Details",
    #             message=f"Welcome! Your username is {teacher.user.username}. Login with the password 'ou@123'. You must change your password within 24 hours.",
    #             from_email="admin@system.com",
    #             recipient_list=[teacher.user.email],
    #             fail_silently=True,
    #         )
    #         return Response({"message": "Teacher account created successfully. Email sent!"},
    #                         status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # @action(methods=['post'], url_path='change-password', detail=True, permission_classes=[IsAuthenticated])
    # def change_password(self, request, pk):
    #     """
    #     Allow teachers to change their password within the 24-hour period.
    #     """
    #     user = User.objects.filter(pk=pk, role=2).first()  # Retrieve only teacher accounts
    #     if not user:
    #         return Response({"error": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)
    #
    #     new_password = request.data.get('new_password')
    #     if not new_password:
    #         return Response({"error": "New password is required."}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     teacher = Teacher.objects.filter(user=user).first()
    #     if teacher.is_password_change_expired():
    #         user.is_active = False
    #         user.save()
    #         return Response({"error": "Password change expired. Contact admin for a reset."},
    #                         status=status.HTTP_403_FORBIDDEN)
    #
    #     # Update password and reset password_reset_time
    #     user.set_password(new_password)
    #     user.save()
    #     teacher.password_reset_time = timezone_now()
    #     teacher.save()
    #
    #     return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
    #
    # @action(methods=['post'], url_path='reset-password-expiry', detail=True, permission_classes=[IsAuthenticated])
    # def reset_password_expiry(self, request, pk):
    #     """
    #     Admin action to reset password expiry for a teacher account.
    #     """
    #     if request.user.role != 0:
    #         return Response({"error": "Only admins can reset password expiry."}, status=status.HTTP_403_FORBIDDEN)
    #
    #     user = User.objects.filter(pk=pk, role=2).first()
    #     if not user:
    #         return Response({"error": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)
    #
    #     teacher = Teacher.objects.filter(user=user).first()
    #     teacher.password_reset_time = timezone_now()  # Reset the expiry time
    #     teacher.save()
    #
    #     return Response({"message": "Password expiry reset successfully."}, status=status.HTTP_200_OK)
