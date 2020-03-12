from .models import MyUser
from rest_framework import serializers


class MyUserSerializers(serializers.ModelSerializer):
    class Meta:
        model=MyUser
        fields='__all__'


