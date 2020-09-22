from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ModelForm
from django import forms
from django.utils import timezone


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
    post_text = models.CharField(max_length=140)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    liked_by = models.ManyToManyField(User, related_name='user_liked_posts')
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.post_text

    def likes_count(self):
        return self.liked_by.all().count()
    
    def liked_by_all(self):
        return self.liked_by.all()

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=140)
    to_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments') 
# Form models here

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        
class PostForm(ModelForm):
    class Meta:
        model = Post 
        fields = ['post_text']
