from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User)
    post_title = models.CharField(max_length = 200)
    post_date = models.DateField(default = timezone.now)
    post_body = models.TextField()

    def __str__(self):
        return self.post_title

class Following(models.Model):
    user = models.ForeignKey(User)
    following = models.CharField(max_length=200)

class FollowedBy(models.Model):
    user = models.ForeignKey(User)
    followed_by = models.CharField(max_length=200)
