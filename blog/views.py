from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from utils.ratelimit import ratelimit
from datetime import timedelta

from .models import Post, Category, Comment
from .forms import PostForm, SearchForm, CommentForm


def home(request):
    post_list = Post.objects.filter(status='published').order_by('-publish_date')
    categories = Category.objects.all()
    recent_posts = Post.objects.filter(status='published').order_by('-publish_date')[:5]
    
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'posts': posts,
        'categories': categories,
        'recent_posts': recent_posts,
    }
    return render(request, 'blog/home.html', context)


@login_required
@ratelimit(max_requests=1, period=timedelta(minutes=5))
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Check if user is rate limited (this happens automatically)
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post has been submitted for review!')
            return redirect('blog:home')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            return redirect('blog:post_detail', slug=post.slug)
    else:
        comment_form = CommentForm()
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'new_comment': new_comment
    })


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published')
    return render(request, 'blog/category_posts.html', {'category': category, 'posts': posts})


@user_passes_test(lambda u: u.is_staff)
def post_review(request):
    pending_posts = Post.objects.filter(status='draft')
    
    if not pending_posts.exists():
        message = "No posts to review" if Post.objects.exists() else "No posts have been created yet"
        return render(request, 'blog/no_posts_to_review.html', {'message': message})
    
    return render(request, 'blog/post_review.html', {'posts': pending_posts})


@user_passes_test(lambda u: u.is_staff)
def approve_post(request, pk):
    try:
        post = Post.objects.get(pk=pk, status='draft')
        post.status = 'published'
        post.save()
        messages.success(request, f'Approved post: {post.title}')
        return redirect('blog:post_review')
    except Post.DoesNotExist:
        messages.error(request, 'Post not found or already reviewed')
        return redirect('blog:post_review')


@user_passes_test(lambda u: u.is_staff)
def reject_post(request, pk):
    try:
        post = Post.objects.get(pk=pk, status='draft')
        post.status = 'rejected'
        post.save()
        messages.success(request, f'Rejected post: {post.title}')
        return redirect('blog:post_review')
    except Post.DoesNotExist:
        messages.error(request, 'Post not found or already reviewed')
        return redirect('blog:post_review')


def search(request):
    form = SearchForm(request.GET or None)
    results = []
    query = None
    
    if form.is_valid():
        query = form.cleaned_data['query']
        category = form.cleaned_data['category']
        date_from = form.cleaned_data['date_from']
        date_to = form.cleaned_data['date_to']
        
        results = Post.objects.filter(status='published')
        
        if query:
            results = results.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query)
            )
            
        if category:
            results = results.filter(category=category)
            
        if date_from:
            results = results.filter(publish_date__gte=date_from)
            
        if date_to:
            results = results.filter(publish_date__lte=date_to)
    
    return render(request, 'blog/search.html', {
        'form': form,
        'results': results,
        'query': query
    })


def about_view(request):
    return render(request, 'blog/about.html')


def privacy_policy(request):
    return render(request, 'blog/privacy_policy.html')