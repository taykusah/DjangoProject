# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Post URLs
    path('', views.post_list, name='post_list'),
    path('my-posts/', views.user_posts, name='user_posts'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    # Comment URLs
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('post/<slug:slug>/comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('post/<slug:slug>/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

    # Reply URLs
    path('post/<slug:slug>/comment/<int:comment_id>/reply/', views.add_reply, name='add_reply'),
    path('post/<slug:slug>/reply/<int:reply_id>/delete/', views.delete_reply, name='delete_reply'),

    # Search URLs
    path('search/', views.search_posts, name='search_posts'),
    path('advanced-search/', views.advanced_search, name='advanced_search'),

    # Moderator URLs
    path('moderator/', views.moderator_dashboard, name='moderator_dashboard'),
]