from django.db import models
from django.db.models.signals import post_save
from django.utils.html import mark_safe
from apps.main.models import Tag, Category
from ckeditor.fields import RichTextField
from apps.account.models import Profile


class Post(models.Model):
    title = models.CharField(max_length=225)
    image = models.ImageField(upload_to='posts/')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def image_tag(self):
        if self.image:
            return mark_safe(f'<a href="{self.image.url}"> <img src="{self.image.url}" style="height:150px;"/> </a>' )
        else:
            return 'Image not found'

    def __str__(self):
        return self.title


class Body(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = RichTextField()
    is_script = models.BooleanField(default=False)

    def __str__(self):
        return f"Body of {self.post}"


class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    top_level_comment_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.author}\'s comment'

    @property
    def get_related_comments(self):
        qs = Comment.objects.filter(top_level_comment_id=self.id).exclude(id=self.id)
        if qs:
            return qs
        return None


def comment_post_save(instance, sender, created, *args, **kwargs):
    if created:
        top_level_comment = instance
        while top_level_comment.parent_comment:
            top_level_comment = top_level_comment.parent_comment
        instance.top_level_comment_id = top_level_comment.id
        instance.save()


post_save.connect(comment_post_save, sender=Comment)

