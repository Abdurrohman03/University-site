from apps.account.models import Profile
from apps.main.models import Category, Tag
from ckeditor.fields import RichTextField
from django.db import models


def image_uploader(instance, filename):
    return f'{instance.title}/{filename}'


class Timestamp(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Course(Timestamp):
    DIFFICULTY = (
        (0, 'Beginner'),
        (1, 'Intermediate'),
        (2, 'Advanced'),
    )
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to=image_uploader)
    title = models.CharField(max_length=225)
    body = RichTextField()
    price = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True)
    discount_price = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True)
    difficulty = models.IntegerField(choices=DIFFICULTY, default=0)
    is_free = models.BooleanField(default=False)

    def __str__(self):
        return self.title



def file_path(instance, filename):
    return f'{instance.lesson.course.title}/{instance.lesson.title}/{filename}'


class Lesson(Timestamp):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=225)
    body = RichTextField()

    def __str__(self):
        return self.title


class LessonFiles(Timestamp):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    file = models.FileField(upload_to=file_path)  # course_name/lesson_name/file
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return self.lesson.title


class SoldCourse(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile.user.username} -> {self.course.title}'

