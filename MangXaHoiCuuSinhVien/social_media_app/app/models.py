from operator import truediv
from tkinter.constants import CASCADE

from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.db import models
from enum import Enum


class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True, null=True)
    updated_date = models.DateField(auto_now=True,null=True)
    deleted_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-id']

class Role(Enum):
    ALUMNI = 'alumni'
    TEACHER ='teacher'

    def choices(cls):
        return [(Role.value, Role.name) for role in cls]

# class Role(BaseModel):
#     role_name = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.role_name


class User(AbstractUser):
    avatar = models.ImageField(upload_to="images/accounts/avatar/%Y/%m", null=True,blank=True)
    gender = models.BooleanField(default=True, null=True)
    role_choices = [
        (1, 'Alumni'),
        (2, 'Teacher'),
    ]
    role = models.IntegerField(
        max_length=255,
        choices=role_choices,
        default=1,
    )
    # phone_number = models.CharField(max_length=255, unique=True, null=True)
    # date_of_birth = models.DateField(null=True)
    # role = models.ForeignKey(Role, on_delete=models.CASCADE)
    # role = models.CharField(max_length=255, choices=Role.choices(), default=Role.ALUMNI.value)

    def __str__(self):
        return self.username


# class Teacher(BaseModel):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)


class Alumni(BaseModel):
    alumni_id = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class AbstractPost(BaseModel):
    class Meta:
        abstract = True
        ordering = ['-id']

    post_content = models.TextField()
    lock_comment = models.BooleanField(default=False)


# class Post(AbstractPost):
#     user = models.ForeignKey(User, on_delete=CASCADE)
