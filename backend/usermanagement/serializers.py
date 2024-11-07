
from rest_framework import serializers

from .models import MyUser

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}