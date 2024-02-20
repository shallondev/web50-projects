import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User, Post
from .forms import CreatePostForm


@login_required
def update_like(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get('post_id')

        try:
            post = Post.objects.get(id=post_id)

            if request.user in post.likes.all():
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)
            
            post.save()
            post_likes = post.likes.all().count()

            return JsonResponse({'success': True, 'post_id': post_id, 'post_likes' : post_likes})
        except Post.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post does not exist'})


@login_required
def update_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get('post_id')
        new_content = data.get('new_content')

        try:
            post = Post.objects.get(id=post_id)
            post.content = new_content
            post.save()
            return JsonResponse({'success': True, 'post_id': post_id, 'new_content': new_content})
        except Post.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post does not exist'})


def view_profile(request, poster, follow=None):

    # Rerieve User object from poster
    poster_user = User.objects.get(username=poster)

    if request.method == "POST":

        if follow == 'true':
            request.user.following.add(poster_user)
            poster_user.followers.add(request.user)
        else:
            request.user.following.remove(poster_user)
            poster_user.followers.remove(request.user)

        return redirect("view_profile", poster=poster)

    # Retrieve Posts by user in reverse chronological order
    posts = Post.objects.filter(poster=poster_user).order_by('-date')

    # Retrieve the number of followers and following
    followers_count = poster_user.followers.count()
    following_count = poster_user.following.count()

    # Paginator
    paginator = Paginator(posts, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/view_profile.html", {
        'profile' : poster_user,
        'followers' : followers_count,
        'following' : following_count,
        'page_obj' : page_obj
    })


@login_required
def create_post(request): 
    if request.method == "POST":
        
        form = CreatePostForm(request.POST)
        
        if form.is_valid():
           
            # Save the form without committing to get the Post object
            post = form.save(commit=False)
           
            # Set the poster field to the current user and save
            post.poster = request.user
            post.save()
        
        # Redirect to index
        return HttpResponseRedirect(reverse("index"))


def index(request, username=None):

    # If username is given
    if username:

        # Get user object model
        current_user = User.objects.get(username=username)

        # Get the list of users the current user is following
        following_users = current_user.following.all()

        # Filter posts by users the current user is following
        posts = Post.objects.filter(poster__in=following_users).order_by('-date')
    
    # Otherwise show all posts
    else:
        posts = Post.objects.order_by('-date')

    # Paginator
    paginator = Paginator(posts, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render index
    return render(request, "network/index.html", {
        'form' : CreatePostForm(),
        'page_obj': page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
