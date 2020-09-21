from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json


# Create your views here.

from .models import User, Post, PostForm, UserForm


def index(request):
    if request.user.is_authenticated:
        user = request.user
        # print('username', user.username)
        # print('following', user.following.all())
        # print('followed by', user.followers.all())
        # print('date joined', user.date_joined)
        posts = Post.objects.order_by('-date').all()
        # for post in posts:
        #     print(post.id, post.liked_by.all())
        # print(posts)
        return render(request, "network/index.html", {'posts':posts})
    else:
        return redirect('login')

# Posts Views

@login_required
def new_post(request):
    if request.method == 'POST':
        new_post = request.POST["new_post"];
        Post.objects.create(user=request.user, post_text=new_post)
        return redirect('index')
    else:
        return redirect('index')

@login_required
def update_post(request, post_id, action):
    if request.method == 'PUT' and action == 'edit':
        post = Post.objects.get(id=post_id)
        data = json.loads(request.body)
        post.post_text = data['newText']
        post.save()
        # return JsonResponse({"success": "Post text updated"})
        return HttpResponse('Success: Post text updated')
    elif request.method == 'PUT' and action == 'likes':
        user = request.user;
        post = Post.objects.get(id=post_id)
        data = json.loads(request.body)
        action = data['action']
        if action == 'Unlike':
            # remove posts liked by the user
            post.liked_by.remove(user)
            # compute the new number of likes and send a json response
            response = {'likes_count': post.liked_by.all().count(),
                        'next_action': 'Like',
                        'message': 'Success - Unlike processed'}
            return JsonResponse(response)
        elif action == 'Like':
            # add posts liked by the user
            post.liked_by.add(user)
             # compute the new number of likes and send a json response
            response = {'likes_count': post.liked_by.all().count(),
                        'next_action': 'Unlike',
                        'message': 'Success - Like processed'}
            return JsonResponse(response)
    else:
        return HttpResponseBadRequest("Error: PUT request required.")


# Authentication Views

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        # https://stackoverflow.com/questions/29588808/django-how-to-check-if-username-already-exists
        if User.objects.filter(username=username).exists():
            return render(request, "network/register.html",
             {"message": "Username already taken."})
        else:
            user = User.objects.create_user(username, email, password)
            # user.first_name = firstname
            # user.last_name = lastname
            user.save()
            return redirect('login')
    else:
        return render(request, "network/register.html")
