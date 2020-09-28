from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
from dateutil import tz
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

from .models import User, Post, Comment, PostForm, UserForm


def index(request):
    if request.user.is_authenticated:
        # user = request.user
        # print('username', user.username)
        # print('following', user.following.all())
        # print('followed by', user.followers.all())
        # print('date joined', user.date_joined)
        posts = Post.objects.order_by('-date').all()
        return render(request, "network/index.html", 
            {'posts':posts})
    else:
        return redirect('login')

def index_pager(request):
    if request.user.is_authenticated:
        posts = Post.objects.order_by('-date').all()
        page = request.GET.get('page', 1)
        paginator = Paginator(posts, 10)
        # page_posts is an instance of the Page class
        # see: https://docs.djangoproject.com/en/3.1/ref/paginator/#django.core.paginator.Paginator
        try:
            page_posts = paginator.page(page)
        except PageNotAnInteger:
            page_posts = paginator.page(1)
        except EmptyPage:
            page_posts = paginator.page(paginator.num_pages)
        return render(request, "network/index_pager.html", 
            {'page_posts':page_posts})
    else:
        return redirect('login')

# Following/Followers

@login_required
def following(request, user_id):
    user = User.objects.get(id=user_id)
    following_users = user.following.all()
    # post_list = [user.user_posts.all() for user in following_users]
    # print(post_list)
    post_id_list = []
    for user in following_users:
        post_ids = [post.id for post in user.user_posts.all()]
        post_id_list += post_ids
    posts = Post.objects.filter(id__in=post_id_list).order_by('-date')
    return render(request, 'network/following.html', {'posts':posts})

@login_required
def following_pager(request, user_id):
    user = User.objects.get(id=user_id)
    following_users = user.following.all()
    # post_list = [user.user_posts.all() for user in following_users]
    # print(post_list)
    post_id_list = []
    for user in following_users:
        post_ids = [post.id for post in user.user_posts.all()]
        post_id_list += post_ids
    posts = Post.objects.filter(id__in=post_id_list).order_by('-date')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page', 1)
        # see: https://docs.djangoproject.com/en/3.1/ref/paginator/#django.core.paginator.Paginator
    try:
        page_posts = paginator.page(page)
    except PageNotAnInteger:
        page_posts = paginator.page(1)
    except EmptyPage:
        page_posts = paginator.page(paginator.num_pages)
    return render(request, 'network/following_pager.html', {'page_posts':page_posts})

@login_required
def followers_pager(request, user_id):
    user = User.objects.get(id=user_id)
    followers_user = user.followers()
    print(user);
    print(followers_user);
    # post_list = [user.user_posts.all() for user in following_users]
    # print(post_list)
    post_id_list = []
    for user in followers_user:
        post_ids = [post.id for post in user.user_posts.all()]
        post_id_list += post_ids
    posts = Post.objects.filter(id__in=post_id_list).order_by('-date')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page', 1)
        # see: https://docs.djangoproject.com/en/3.1/ref/paginator/#django.core.paginator.Paginator
    try:
        page_posts = paginator.page(page)
    except PageNotAnInteger:
        page_posts = paginator.page(1)
    except EmptyPage:
        page_posts = paginator.page(paginator.num_pages)
    return render(request, 'network/followers_pager.html', {'page_posts':page_posts})

# Profile

@login_required
def profile(request, user_id):
    post_user = User.objects.get(id=user_id)
    user_posts = Post.objects.filter(user=post_user).order_by('-date')
    followers = post_user.followers()
    following = post_user.following.all()
    context = {'followers':followers, 'following':following, 
               'post_user':post_user, 'user_posts': user_posts}
    return render(request, 'network/profile.html', context)

@login_required
def profile_pager(request, user_id):
    post_user = User.objects.get(id=user_id)
    user_posts = Post.objects.filter(user=post_user).order_by('-date')
    followers = post_user.followers()
    following = post_user.following.all()
    paginator = Paginator(user_posts, 10)
    page = request.GET.get('page', 1)
        # see: https://docs.djangoproject.com/en/3.1/ref/paginator/#django.core.paginator.Paginator
    try:
        page_posts = paginator.page(page)
    except PageNotAnInteger:
        page_posts = paginator.page(1)
    except EmptyPage:
        page_posts = paginator.page(paginator.num_pages)
    context = {'followers':followers, 'following':following, 
               'post_user':post_user, 'page_posts': page_posts}
    return render(request, 'network/profile_pager.html', context)

# Post Comments
@login_required
def comments(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = post.post_comments.all()
    to_zone = tz.tzlocal()
    comment_list = [{'id':comment.id, 
                    'text':comment.text, 
                    'date':comment.date.astimezone(tz.tzlocal()),
                    'post':comment.to_post.id} for comment in comments]
    # print(comment_list)
    response = JsonResponse(comment_list, safe=False)
    return redirect('index')

@login_required
def delete_comment(request, post_id, comment_id):
    if request.method == "DELETE":
        post = Post.objects.get(id=post_id)
        comment = Comment.objects.get(id=comment_id)
        # print(post.post_comments.all());
        comment.delete()
        # print(post.post_comments.all());
        return JsonResponse({'message': 'Success: Comment deleted'});

# Post Actions

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        body = json.loads(request.body)
        text = body['comment']
        # print(post_id)
        post = Post.objects.get(id=post_id)
        Comment.objects.create(text=text, to_post=post);
        comment_list = list(Comment.objects.filter(to_post=post_id))
        last_comment = comment_list[-1]
        comment_id = last_comment.id;
        current_user = request.user.username;
        post_user = post.user.username;
        return JsonResponse({'message': 'Success: Comment added to post',
                             'date': last_comment.date,
                             'current_user': current_user,
                             'post_user': post_user,
                             'comment_id': comment_id})

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

@login_required
def update_user(request, user_id, action):
    if request.method == 'PUT' and action == 'follow':
        current_user = request.user;
        user = User.objects.get(id=user_id)
        print('user to be processed', user.username)
        data = json.loads(request.body)
        action = data['action']
        if action == 'Follow' and current_user != user:
            # print(f'add {user} from {current_user} following set')
            current_user.following.add(user)
        elif action == 'Unfollow' and current_user != user:
            # print(f'remove {user} from {current_user} following set')
            current_user.following.remove(user)
        return HttpResponse('Success: Post following set updated')
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
