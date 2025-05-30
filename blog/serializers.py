from rest_framework import serializers
from .models import Post, Category, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author', 'category', 
                 'content', 'publish_date', 'status']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'text', 'created_date']