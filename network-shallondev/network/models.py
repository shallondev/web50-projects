from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')

    def __str__(self):
        return self.username


class Post(models.Model):
    content = models.TextField(max_length=100)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, symmetrical=False, related_name='liked')

    # State poster and date for django admin 
    def __str__(self):
        return f"{self.poster} posted on {self.date} and said: {self.content}"

    # Test if the post is valid
    def has_content(self):
        return bool(self.content)