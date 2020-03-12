from .models import Post,Comment
from rest_framework import serializers

class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model=Post
        # fields="__all__"
        exclude=['user']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields="__all__"


