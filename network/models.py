from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ModelForm
from django import forms
from django.utils import timezone
from dateutil import tz


class User(AbstractUser):
    following = models.ManyToManyField('self', symmetrical=False, 
                blank=True, related_name='followers')
    
    def __str__(self):
        return self.username

    def following_all(self):
        return self.following.all();

    def following_count(self):
        return self.following.all().count()

    def followers_count(self):
        return self.followers.all().count()


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    post_text = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    liked_by = models.ManyToManyField(User, related_name='user_liked_posts', blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.post_text

    def likes_count(self):
        return self.liked_by.all().count()
    
    def liked_by_all(self):
        return self.liked_by.all()

    def comments_count(self):
        return self.post_comments.all().count()

    def comments(self):
        all_comments = self.post_comments.all()
        comment_list = []
        for comment in all_comments:
            dict = {}
            dict['id'] = comment.id
            comment.date = comment.date.astimezone(tz.tzlocal())
            dict['new_date'] = comment.date.astimezone(tz.tzlocal())
            dict['to_post'] = comment.to_post
            dict['text'] = comment.text 
            comment_list.append(dict)
        # comment_list = [{'text': comment.text, 'to_post':comment.to_post,
        #                  'date': comment.date.astimezone(tz.tzlocal()),
        #                  'id': comment.id} 
        #                  for comment in all_comments]
        return comment_list

class Comment(models.Model):
    text = models.CharField(max_length=500)
    to_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments') 
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text[0:30]

# Form models here

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        
class PostForm(ModelForm):
    class Meta:
        model = Post 
        fields = ['post_text']
