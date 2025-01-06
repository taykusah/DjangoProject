# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'comments', views.CommentViewSet, basename='comment')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]