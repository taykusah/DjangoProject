# api/serializers.py
from rest_framework import serializers
from blog.models import Post, Category, Comment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author', 'content', 
                 'category', 'category_id', 'created_at', 
                 'updated_at', 'image', 'status', 'comments']
        read_only_fields = ['slug']