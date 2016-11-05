from rest_framework import serializers
from app01.models import Activity, User, UserActivity

class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('id', 'user_name', 'email', 'first_name', 'last_name', 'password', 'gender', 'height', 'weight', 'birthday')