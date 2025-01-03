from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField
from enum import IntEnum

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True,null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ["-id"]


class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=False, blank=False)
    cover_avatar = CloudinaryField('cover-avatar', null=True, blank=True)
    gender = models.BooleanField(default=True, null=True)
    email = models.EmailField(unique=True, null=False, max_length=254)
    role_choices = [
        (1, 'Alumni'),
        (2, 'Teacher'),
    ]
    role = models.IntegerField(
        choices=role_choices,
        default=1,
    )

    register_form = models.OneToOneField('RegisterForm', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username


class RegisterForm(BaseModel):
    alumni_code = models.CharField(max_length=10, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255, default="ou@123")
    email = models.EmailField(unique=True, null=False, max_length=255)
    avatar = CloudinaryField('avatar', null=False, blank=True)
    cover_avatar = CloudinaryField('cover_avatar', null=True, blank=True)
    gender = models.BooleanField(default=True, null=True)

    def __str__(self):
        return self.alumni_code

class Post(BaseModel):
    content = models.TextField()
    lock_comment = models.BooleanField(default=False)

    user = models.ForeignKey(User,on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.content

class PostImage(models.Model):
    image = CloudinaryField('Post Image', null=True, blank=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class SurveyPost(Post):
    end_time = models.DateTimeField()


class SurveyType(IntEnum):
    TRAINING_PROGRAM = 1
    RECRUITMENT_INFORMATION = 2
    INCOME = 3
    EMPLOYMENT_SITUATION = 4

    @classmethod
    def choices(cls):
        return [(type.value, type.name.replace('_', ' ').capitalize()) for type in cls]


class SurveyQuestionType(models.Model):
    type_survey = models.IntegerField(choices=SurveyType.choices(),
                                      default=SurveyType.TRAINING_PROGRAM.value)

    def __str__(self):
        return str(self.type_survey)


class SurveyQuestion(models.Model):
    question = models.TextField()

    survey_post = models.ForeignKey(SurveyPost,  on_delete=models.CASCADE)
    survey_question_type = models.ForeignKey(SurveyQuestionType, on_delete=models.CASCADE)

    def __str__(self):
        return self.question


class SurveyOption(models.Model):
    option = models.TextField()
    multi_choices = models.BooleanField(default=False)

    survey_question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    user = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.option


class Group(BaseModel):
    group_name = models.CharField(max_length=255, unique=True)

    user = models.ManyToManyField(User,blank=True)

    def __str__(self):
        return self.group_name


class InvitationPost(Post):
    event_name = models.CharField(max_length=255)

    invitation_users = models.ManyToManyField(User, blank=True)
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
        return str(self.reaction)


class Comment(Interaction):
    content = models.TextField(null=False)
    image = CloudinaryField('Comment Images', null=True, blank=True)

    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.content