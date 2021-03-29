from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    photo = models.URLField(max_length=200, blank=True)
    bio = models.CharField(max_length=1000, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    influences = models.CharField(max_length=1000, blank=True)
    why = models.CharField(max_length=1000, blank=True)
    what = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.username

class Paper(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=100000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    
    def __str__(self):
        return f"{self.title}: {self.author}"

    def serialize(self):
        return {
            "title": self.title,
            "content": self.content,
            "author": self.author.username
        }

class Comment(models.Model):
    content = models.CharField(max_length=1000)
    time_stamp = models.DateTimeField(auto_now_add=True)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    selection = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return f"{self.commenter}: {self.time_stamp}"

class Community(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, default=None, related_name="members")

    def __str__(self):
        return self.name
    