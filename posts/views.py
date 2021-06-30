from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User, Comment, Follow
from django.http import HttpResponse
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render
import datetime as dt, datetime
from django.views.decorators.cache import cache_page


@cache_page(60 / 3)
def index(request): 
    paginator = Paginator(Post.objects.all(), 10)
    page_number = request.GET.get("page")  
    page = paginator.get_page(page_number)  
    return render(request, "index.html",
        {
        "page": page, 
        "paginator": paginator
        })

def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts_count = group.posts.count()
    date_posts = Post.objects.filter(group=group).order_by("-pub_date")
    paginator = Paginator(date_posts, 5)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "group.html", 
        {"group": group, 
        "page": page,   
        "paginator": paginator, 
        "posts_count": posts_count,
        })

@login_required
def new_post(request):
    if not request.method == "POST":
        form = PostForm()
        return render(request, "new.html", {"form": form}) 
    form = PostForm(request.POST, files=request.FILES or None)
    if not form.is_valid():
        return render(request, "new.html", {"form": form})
    post_get = form.save(commit=False)
    post_get.author = request.user
    post_get.save()
    return redirect("/")
    
def profile(request, username):
    author = get_object_or_404(User, username=username)
    author_posts = author.posts.all()
    count_posts = author_posts.count()
    followers = Follow.objects.filter(author=author)
    count_followers = followers.count()
    followings = Follow.objects.filter(user=author)
    count_followings = followings.count()
    following = False
    if request.user.is_authenticated:
        if Follow.objects.filter(user=request.user,
                                 author=author).exists():     
            following = True
    paginator = Paginator(author_posts, 5)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "profile.html",
                  {"page": page,
                   "paginator": paginator,
                   "count_posts": count_posts,
                   "author": author,
                   "count_followers": count_followers,
                   "count_followings": count_followings,
                   "following": following})
 
def post_view(request, username, post_id):
    users = User.objects.get(username=username)
    post = get_object_or_404(Post, author__username=username, id=post_id)
    post_list = Post.objects.filter(author=users)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    posts_count = users.posts.count()
    form = CommentForm(instance=None)  
    comments_count = Comment.objects.filter(post_id=post_id).count()
    comments = Comment.objects.filter(post_id=post_id)
    return render(request, "post.html", 
        {
        "page": page, 
        "paginator": paginator, 
        "users": users, 
        "post": post,
        "posts_count": posts_count,
        "comments" : comments,
        "comments_count": comments_count,
        "form": form
        })

def post_edit(request, username, post_id):
    post = get_object_or_404(
        Post, author=User.objects.get(username=username),
        pk=post_id
        )
    if post.author != request.user:
        return redirect("post", username=username, post_id=post_id)
    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post
        )
    if form.is_valid():
        form.save(commit=False)
        form.save()
        return redirect("post", username=username, post_id=post_id)
    return render(
        request,
        "new.html",
        {
            "form": form,
            "post": post,
            "username": username,
            "post_id": post_id,
            "author": request.user
        }
    )

def page_not_found(request, exception):
    return render(
        request, 
        "misc/404.html", 
        {"path": request.path}, 
        status=404
    )

def server_error(request):
    return render(request, "misc/500.html", status=500)

@login_required
def add_comment(request, username, post_id):
    post_author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    form = CommentForm(request.POST or None)
    items = post.comments.all()
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect("post", username=username, post_id=post_id)
    context = {
        "form": form,
        "post_author": post_author,
        "post": post,
        "items": items,}
    return render(request, "comments.html", context)

@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
                 request, 
                 "follow.html", 
                 {"page": page, "paginator": paginator, 'post_list': post_list}
                 )
 
@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect("profile", username=username)
 
@login_required
def profile_unfollow(request, username):
    unfollow_profile = Follow.objects.get(
        author__username=username, user=request.user
        )
    if Follow.objects.filter(pk=unfollow_profile.pk).exists():
        unfollow_profile.delete()
    return redirect("profile", username=username)
