from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Post, Category
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SearchForm
from django.db.models import Q
from .forms import CommentForm
from .models import Comment


def home(request):
    posts = Post.objects.filter(status='published').order_by('-publish_date')
    categories = Category.objects.all()
    recent_posts = Post.objects.filter(status='published').order_by('-publish_date')[:5]
    
    context = {
        'posts': posts,
        'categories': categories,
        'recent_posts': recent_posts,
    }
    return render(request, 'blog/home.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
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
    return render(request, 'blog/post_detail.html', {'post': post})

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published')
    return render(request, 'blog/category_posts.html', {'category': category, 'posts': posts})


@user_passes_test(lambda u: u.is_staff)
def post_review(request):
    # Try both common draft status variations
    pending_posts = Post.objects.filter(status__in=['draft', 'pending'])
    
    if not pending_posts.exists():
        # Check if there are any posts at all
        if Post.objects.exists():
            # Posts exist but none are draft/pending
            message = "All posts have been reviewed."
        else:
            # No posts exist in the system
            message = "No posts have been created yet."
        return render(request, 'blog/no_posts_to_review.html', {'message': message})
    
    return render(request, 'blog/post_review.html', {'posts': pending_posts})

@user_passes_test(lambda u: u.is_staff)
def approve_post(request, pk):
    try:
        post = Post.objects.get(pk=pk, status__in=['draft', 'pending'])
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
        post = Post.objects.get(pk=pk, status__in=['draft', 'pending'])
        post.status = 'rejected'
        post.save()
        messages.success(request, f'Rejected post: {post.title}')
        return redirect('blog:post_review')
    except Post.DoesNotExist:
        messages.error(request, 'Post not found or already reviewed')
        return redirect('blog:post_review')

def privacy_policy(request):
    return render(request, 'blog/privacy_policy.html')

def home(request):
    post_list = Post.objects.filter(status='published').order_by('-publish_date')
    categories = Category.objects.all()
    recent_posts = Post.objects.filter(status='published').order_by('-publish_date')[:5]
    
    # Pagination
    paginator = Paginator(post_list, 5)  # Show 5 posts per page
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

def search(request):
    form = SearchForm()
    results = []
        
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query),
                status='published'
            ).distinct()
        
        return render(request, 'blog/search.html', {
            'form': form,
            'results': results,
            'query': request.GET.get('query', '')
        })        

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

def about_view(request):
    return render(request, 'blog/about.html')