from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, Follow
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.http import HttpResponseForbidden


User = get_user_model()

ITEMS_PER_PAGE = 10


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.all().filter(group=group)
    paginator = Paginator(post_list, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


# @cache_page(20, key_prefix='index_page')
def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def profile(request, username):
    author = User.objects.get(username=username)
    user_posts = Post.objects.all().filter(author=author)
    post_count = Post.objects.all().filter(author=author).count()
    paginator = Paginator(user_posts, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    following = False
    if request.user.is_authenticated:
        if request.user != author.username:
            following = Follow.objects.filter(user=request.user, author=author).exists()
    context = {
        'post_count': post_count,
        'page_obj': page_obj,
        'author': author,
        'following': following,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post_info = get_object_or_404(Post, pk=post_id)
    form = CommentForm()
    comments = post_info.comments.all()
    context = {
        'post_info': post_info,
        'form': form,
        'comments': comments
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        form.save(commit=False).author_id = request.user.pk
        form.save()
        return redirect(
            'posts:profile', username=request.user.username
        )
    return render(request, template, {'form': form, 'is_edit': False})


@login_required
def post_edit(request, post_id):
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )

    if post.author != request.user:
        return HttpResponseForbidden()

    if form.is_valid():
        form.save()
        return redirect(
            'posts:post_detail', post_id
        )
    context = {
        'form': form,
        'is_edit': True,
        'post': post,
    }
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    template = 'posts/follow.html'
    posts = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(posts, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    follow_author = get_object_or_404(User, username=username)
    if follow_author != request.user and (
        not request.user.follower.filter(author=follow_author).exists()
    ):
        Follow.objects.create(
            user=request.user,
            author=follow_author
        )
    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request, username):
    follow_author = get_object_or_404(User, username=username)
    data_follow = request.user.follower.filter(author=follow_author)
    if data_follow.exists():
        data_follow.delete()
    return redirect('posts:profile', username)
