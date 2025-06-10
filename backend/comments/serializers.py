from rest_framework import serializers
from .models import Comment


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    replies = ReplySerializer(many=True, read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'parent', 'created_at', 'replies']
        read_only_fields = ['author', 'created_at']
        
