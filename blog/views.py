# blog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from .models import Post, Category, Comment, Reply
from .forms import PostForm, CommentForm
from .mixins import AuthorRequiredMixin, ModeratorRequiredMixin

def post_list(request):
    posts = Post.objects.filter(status='published').order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'categories': categories
    })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.filter(parent=None).order_by('-created_at')
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments
    })

@login_required
def post_create(request):
    if not request.user.profile.is_author:
        messages.error(request, "You don't have permission to create posts.")
        return redirect('blog:post_list')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Create Post'})

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not (request.user == post.author or request.user.profile.is_moderator):
        messages.error(request, "You don't have permission to edit this post.")
        return redirect('blog:post_detail', slug=slug)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Edit Post'})

class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to delete this post.")
        return redirect('blog:post_detail', slug=self.get_object().slug)

@login_required
def user_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/user_posts.html', {
        'posts': posts,
        'title': 'My Posts'
    })

@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Error adding comment. Please try again.')
    return redirect('blog:post_detail', slug=slug)

@login_required
def edit_comment(request, slug, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'content': comment.content})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def delete_comment(request, slug, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if not (request.user == comment.author or request.user.profile.is_moderator):
        messages.error(request, "You don't have permission to delete this comment.")
        return redirect('blog:post_detail', slug=slug)
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
    return redirect('blog:post_detail', slug=slug)

@login_required
def add_reply(request, slug, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Reply.objects.create(
                comment=comment,
                author=request.user,
                content=content
            )
            messages.success(request, 'Reply added successfully!')
        else:
            messages.error(request, 'Reply content cannot be empty.')
    return redirect('blog:post_detail', slug=slug)

@login_required
def delete_reply(request, slug, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    if not (request.user == reply.author or request.user.profile.is_moderator):
        messages.error(request, "You don't have permission to delete this reply.")
        return redirect('blog:post_detail', slug=slug)
    
    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Reply deleted successfully!')
    return redirect('blog:post_detail', slug=slug)

def search_posts(request):
    query = request.GET.get('q', '')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query),
            status='published'
        ).distinct()
    else:
        posts = []
    
    return render(request, 'blog/search_results.html', {
        'posts': posts,
        'query': query
    })

def advanced_search(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    date_filter = request.GET.get('date_filter', '')
    sort_by = request.GET.get('sort_by', '-created_at')
    
    # Base queryset
    posts = Post.objects.filter(status='published')
    
    # Search in title and content
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )
    
    # Category filter
    if category:
        posts = posts.filter(category__slug=category)
    
    # Date filter
    if date_filter:
        today = datetime.now()
        if date_filter == 'today':
            posts = posts.filter(created_at__date=today.date())
        elif date_filter == 'week':
            week_ago = today - timedelta(days=7)
            posts = posts.filter(created_at__gte=week_ago)
        elif date_filter == 'month':
            month_ago = today - timedelta(days=30)
            posts = posts.filter(created_at__gte=month_ago)
        elif date_filter == 'year':
            year_ago = today - timedelta(days=365)
            posts = posts.filter(created_at__gte=year_ago)
    
    # Sorting
    if sort_by in ['-created_at', 'created_at', '-title', 'title']:
        posts = posts.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(posts, 9)  # 9 posts per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for the filter dropdown
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'selected_category': category,
        'date_filter': date_filter,
        'sort_by': sort_by,
        'categories': categories,
        'total_results': paginator.count,
    }
    
    return render(request, 'blog/search.html', context)

@login_required
def moderator_dashboard(request):
    if not request.user.profile.is_moderator:
        messages.error(request, "You don't have permission to access the moderator dashboard.")
        return redirect('home')
    
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/moderator_dashboard.html', {'posts': posts})