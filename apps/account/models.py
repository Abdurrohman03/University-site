from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe


def image_path(instance, filename):
    return f'{instance.user.username}/{filename}'


class Profile(models.Model):
    ROLE = (
        (0, 'Student'),
        (1, 'Teacher'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_path, null=True, blank=True)
    bio = RichTextField(null=True, blank=True)
    role = models.IntegerField(choices=ROLE, default=0)

    def __str__(self):
        return self.user.username

    def image_tag(self):
        if self.image:
            return mark_safe(f'<a href="{self.image.url}"> <img src="{self.image.url}" style="height:150px;"/> </a>' )
        else:
            return 'Image not found'


def user_post_save(instance, sender, created, *args, **kwargs):
    if created:
        Profile.objects.create(user_id=instance.id)


post_save.connect(user_post_save, sender=User)
