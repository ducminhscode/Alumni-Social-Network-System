from rest_framework.serializers import ModelSerializer, ValidationError, CharField, EmailField, URLField
from .models import User, Alumni, Teacher


class UserSerializer(ModelSerializer):

    def create(self, validated_data):
        data = validated_data.copy()
        u = User(**data)
        u.role = 1
        u.set_password(u.password)
        u.save()
        return u


    class Meta:
        model = User
        fields = ["id", "username", "password", "avatar", "cover", "first_name", "last_name", "email"]
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class AlumniSerializer(ModelSerializer):
    username = CharField(write_only=True)
    email = EmailField(write_only=True)
    password = CharField(write_only=True, required=False, default='ou@123')
    avatar = URLField(write_only=True)
    cover = URLField(write_only=True)
    first_name=CharField(write_only=True)
    last_name = CharField(write_only=True)


    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email = validated_data.pop('email')
        avatar = validated_data.pop('avatar')
        cover = validated_data.pop('cover')
        student_code = validated_data.pop('student_code')

        if not avatar:
            raise ValidationError({"avatar": "Chọn Avatar"})

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            avatar=avatar,
            cover=cover,
            role=1
        )

        alumni = Alumni.objects.create(user=user, student_code=student_code)
        return alumni

    class Meta:
        model = Alumni
        fields = ["id", "username", "password", "first_name", "last_name", "email", "avatar", "cover", "student_code"]


class TeacherSerializer(ModelSerializer):
    username = CharField(write_only=True)
    email = EmailField(write_only=True)
    password = CharField(write_only=True, required=False, default='ou@123')
    avatar = URLField(write_only=True)
    cover = URLField(write_only=True)
    first_name=CharField(write_only=True)
    last_name = CharField(write_only=True)


    def create(self, validated_data):
        username = validated_data.pop('username')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email = validated_data.pop('email')
        avatar = validated_data.pop('avatar')
        cover = validated_data.pop('cover')

        if not avatar:
            raise ValidationError({"avatar": "Chọn Avatar"})

        user = User.objects.create_user(
            username=username,
            password='ou@123',
            first_name=first_name,
            last_name=last_name,
            email=email,
            avatar=avatar,
            cover=cover,
            role=2
        )

        teacher = Teacher.objects.create(user=user)
        return teacher

    class Meta:
        model = Teacher
        fields = ["id", "username","password", "first_name", "last_name", "email", "avatar", "cover"]
