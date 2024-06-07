from django.contrib.auth import get_user_model
from rest_framework import serializers
from api.models import FriendRequest
from django.contrib.auth.hashers import make_password
User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('last_login', 'groups', 'user_permissions','is_staff','is_superuser','is_active')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        email = validated_data['email'].lower()
        validated_data['email'] = email
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.ReadOnlyField(source='from_user.email')
    to_user = serializers.ReadOnlyField(source='to_user.email')

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']
