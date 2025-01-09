from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField
from enum import IntEnum
from django.utils import timezone




class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True,null=True)
    deleted_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ["-id"]

    def soft_delete(self, using=None, keep_parents=False):
        self.deleted_date = timezone.now()
        self.active = False
        self.save()


class Role(IntEnum):
    ADMIN = 0
    ALUMNI = 1
    TEACHER = 2

    @classmethod
    def choices(cls):
        return [(role.value, role.name.capitalize()) for role in cls]


class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=False, blank=False, folder='lthd',
        default='https://res.cloudinary.com/dqw4mc8dg/image/upload/v1736348093/aj6sc6isvelwkotlo1vw_zxmebm.png')
    cover = CloudinaryField('cover', null=True, blank=True, folder='lthd')
    email = models.EmailField(unique=True, null=False, max_length=255)
    role = models.IntegerField(
        choices=Role.choices(),
        default=Role.ADMIN.value
    )


class Alumni(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_code = models.CharField(max_length=10, unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    must_change_password = models.BooleanField(default=True)
    password_reset_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.user)

    def is_password_change_expired(self):
        if not self.password_reset_time:
            return False
        return (timezone.now() - self.password_reset_time).total_seconds() > 86400


class Post(BaseModel):
    content = models.TextField()
    lock_comment = models.BooleanField(default=False)

    user = models.ForeignKey(User,on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.content

class PostImage(models.Model):
    image = CloudinaryField('Post Image', null=True, blank=True, folder='lthd')

    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class SurveyType(IntEnum):
    TRAINING_PROGRAM = 1
    RECRUITMENT_INFORMATION = 2
    INCOME = 3
    EMPLOYMENT_SITUATION = 4

    @classmethod
    def choices(cls):
        return [(type.value, type.name.replace('_', ' ').capitalize()) for type in cls]


class SurveyPost(Post):
    end_time = models.DateTimeField()
    survey_type = models.IntegerField(choices=SurveyType.choices(),
                                        default=SurveyType.TRAINING_PROGRAM.value)
    def __str__(self):
        return f"{self.content} - {SurveyType(self.survey_type).name.capitalize()}"


class SurveyQuestion(models.Model):
    question = models.TextField()
    multi_choice = models.BooleanField(default=False)

    survey_post = models.ForeignKey(SurveyPost,  on_delete=models.CASCADE)

    def __str__(self):
        return self.question


class SurveyOption(models.Model):
    option = models.TextField()

    survey_question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.option


class Group(BaseModel):
    group_name = models.CharField(max_length=255, unique=True)

    users = models.ManyToManyField(User,blank=True)

    def __str__(self):
        return self.group_name


class InvitationPost(Post):
    event_name = models.CharField(max_length=255)

    users = models.ManyToManyField(User, blank=True)
    groups = models.ManyToManyField(Group, blank=True)

    def __str__(self):
        return self.event_name


class Interaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class ReactionType(IntEnum):
    LIKE = 1
    HAHA = 2
    LOVE = 3

    @classmethod
    def choices(cls):
        return [(reaction.value, reaction.name.capitalize()) for reaction in cls]


class Reaction(Interaction):
    reaction = models.IntegerField(choices=ReactionType.choices(), default=ReactionType.LIKE.value)

    class Meta:
        unique_together = ('user','post')

    def __str__(self):
        return f"{self.user.username} - {ReactionType(self.reaction).name} on Post {self.post.id}"


class Comment(Interaction):
    content = models.TextField(null=False)
    image = CloudinaryField('Comment Images', null=True, blank=True, folder='lthd')

    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def get_replies(self):
        return Comment.objects.filter(parent=self).order_by("created_date")

    def __str__(self):
        if self.parent:
            return f"Reply to {self.parent.id} - {self.content[:30]}"
        return self.content[:30]