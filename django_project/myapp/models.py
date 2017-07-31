# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid


# Create your models here.
class usermode(models.Model):

    name= models.CharField(max_length=255)
    username= models.CharField(max_length=30)
    phone= models.CharField(max_length=20)
    created_on= models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    email= models.EmailField(max_length=20)
    password=models.CharField(max_length=30)


class sessiontoken(models.Model):
    user=models.ForeignKey(usermode)
    session_token=models.CharField(max_length=255)
    created_on=models.DateTimeField(auto_now_add=True)
    is_valid=models.BooleanField(default=True)
    def create_token(self):
        self.session_token=uuid.uuid4()
#post model use to post
class PostModel(models.Model):
    user = models.ForeignKey(usermode)
    image = models.FileField(upload_to='user_images')
    image_url = models.CharField(max_length=255)
    caption = models.CharField(max_length=240)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    has_liked=False

    @property
    def like_count(self):
        return len(LikeModel.objects.filter(post=self))
    @property
    def comments(self):
        return CommentModel.objects.filter(post=self).order_by('created_on')

#like model to like the posts of the user 
class LikeModel(models.Model):
    user = models.ForeignKey(usermode)
    post = models.ForeignKey(PostModel)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

#comments on user posts
class CommentModel(models.Model):
    user = models.ForeignKey(usermode)
    post = models.ForeignKey(PostModel)
    comment_text = models.CharField(max_length=555)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    upvoted = False

    @property
    def upvote(self):
        return len(LikeComm.objects.filter(comment=self))

