from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Alumni, Teacher


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'confirm_password']


    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Mật khẩu không khớp."})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user


class AlumniSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Alumni
        fields = ['user', 'student_code']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        user.role = 1

        alumni = Alumni.objects.create(user=user, **validated_data)
        return alumni

# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'first_name', 'last_name']
#
#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ['user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        user.role = 2
        teacher = Teacher.objects.create(user=user, password_reset_time=timezone.now())
        return teacher