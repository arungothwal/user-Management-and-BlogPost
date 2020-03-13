from .models import Post,Comment
from rest_framework import serializers

# from rest.models import MyUser


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model=Post
        # fields="__all__"
        exclude=['user']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields="__all__"


################### using two serializer in one ######################

class Get_commentSerializers(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    class Meta:
        model=Post
        # model=MyUser
        # fields='__all__'
        fields=['title','description','created_post','comments',]