from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils import timezone
from blog.models import Post, Comment
from .forms import PostForm, CommentForm, SummerForm
from django.shortcuts import redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def post_list(request, HasTag=None):
    posts_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(posts_list, 5)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 페이지가 정수가 아닌 경우 1페이지 출력
        posts = paginator.page(1)
    except EmptyPage:
        # 페이지 범위가 넘어가면 맨 마지막 페이지 출력
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, published_date__lte=timezone.now())

    prev_post = Post.objects.filter(pk__lt=post.pk, published_date__isnull=True).order_by('-pk')
    next_post = Post.objects.filter(pk__gt=post.pk, published_date__isnull=True).order_by('pk')

    return render(request, 'blog/post_detail.html', {'post': post, 'prev_post': prev_post, 'next_post': next_post})


@login_required
def post_draft_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, published_date__isnull=True)

    prev_post = Post.objects.filter(pk__lt=post.pk, published_date__isnull=True).order_by('-pk')
    next_post = Post.objects.filter(pk__gt=post.pk, published_date__isnull=True).order_by('pk')

    return render(request, 'blog/post_detail.html', {'post': post, 'prev_post': prev_post, 'next_post': next_post})


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_draft_detail', pk=post.pk)
    else:
        form = PostForm()
        # form = SummerForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    posts_list = Post.objects.filter(published_date__isnull=True).order_by('-create_date')
    paginator = Paginator(posts_list, 5)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 페이지가 정수가 아닌 경우 1페이지 출력
        posts = paginator.page(1)
    except EmptyPage:
        # 페이지 범위가 넘어가면 맨 마지막 페이지 출력
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.published_date:
        redirectUrl = 'post_list'
    else:
        redirectUrl = 'post_draft_list'

    post.delete()
    return redirect(redirectUrl)


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)
