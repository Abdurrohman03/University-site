from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=225)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=225)

    def __str__(self):
        return self.title


class FAQ(models.Model):
    question = models.CharField(max_length=225)

    def __str__(self):
        return self.question


class Answer(models.Model):
    question = models.ForeignKey(FAQ, on_delete=models.CASCADE)
    answer = models.TextField()

    def __str__(self):
        return f'answer for {self.question}'


class Subscribe(models.Model):
    email = models.EmailField(unique=True, db_index=True)

    def __str__(self):
        return self.email


class Contact(models.Model):
    name = models.CharField(max_length=225)
    email = models.EmailField(max_length=225)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


