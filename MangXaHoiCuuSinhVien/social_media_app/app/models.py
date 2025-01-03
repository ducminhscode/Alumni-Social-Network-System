from operator import truediv
from tkinter.constants import CASCADE

from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField

class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True, null=True)
    updated_date = models.DateField(auto_now=True,null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ["-id"]


class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=False,blank=True)
    cover_avatar = CloudinaryField('cover-avatar', null=True, blank=True)
    gender = models.BooleanField(default=True, null=True)
    role_choices = [
        (1, 'Alumni'),
        (2, 'Teacher'),
    ]
    role = models.IntegerField(
        choices=role_choices,
        default=1,
    )

    def __str__(self):
        return self.username
    

class RegisterRequest(models.Model):
    alumni_id = models.CharField(max_length=255)
    is_pending = models.BooleanField(default=True)

    user = models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True)


class Post(BaseModel):
    content = models.TextField()
    lock_comment = models.BooleanField(default=False)

    user = models.ForeignKey(User,on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.content

class PostImage(models.Model):
    image = CloudinaryField('Post Image', null=True, blank=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, primary_key=True)


class SurveyPost(Post):
    end_time = models.DateTimeField()
    is_closed = models.BooleanField(default=False)


class SurveyQuestionType(models.Model):
    type_choices = [
        (1, 'Training Program'),
        (2, 'Recruitment Information'),
        (3, 'Income'),
        (4, 'Employment Situation')
    ]
    type_survey = models.IntegerField(
        choices=type_choices,
        default=1,
    )

    def __str__(self):
        return self.type_survey


class SurveyQuestion(models.Model):
    content_question = models.TextField()

    survey_post = models.ForeignKey(SurveyPost,  on_delete=models.CASCADE)
    survey_question_type = models.ForeignKey(SurveyQuestionType, on_delete=models.CASCADE)

    def __str__(self):
        return self.content_question


class SurveyQuestionOption(models.Model):
    option_value = models.TextField()
    multi_choices = models.BooleanField(default=False)

    survey_question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    user = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.option_value


class Group(models.Model):
    name = models.CharField(max_length=255)

    user = models.ManyToManyField(User,blank=True)

    def __str__(self):
        return self.name


class InvitationPost(Post):
    event_name = models.CharField(max_length=255)

    invitation_users = models.ManyToManyField(User,blank=True)
    groups = models.ManyToManyField(Group, blank=True)

    def __str__(self):
        return self.event_name


class Interaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Reaction(Interaction):
    reaction_choices = [
        (1, 'Like'),
        (2, 'Haha'),
        (3, 'Love')
    ]
    reaction = models.IntegerField(
        choices=reaction_choices,
        default=1,
    )

    class Meta:
        unique_together = ('user','post')

    def __str__(self):
        return self.reaction


class Comment(Interaction):
    content = models.TextField(null=False)
    image = CloudinaryField('Comment Images', null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.content

