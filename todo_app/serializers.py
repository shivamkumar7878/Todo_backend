from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User
from .utils import is_email_unique

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'username')

    def validate(self, attrs):
        # checking if email is unique across all users
        received_email = attrs.get('email')
        if received_email and is_email_unique(received_email) :
            raise serializers.ValidationError({"email": "User with this email already exists."})

        return attrs

    def create(self, validated_data):
        # create the password hash before savings
        validated_data['password'] = make_password(validated_data['password'])

        # create the client instance
        return super().create(validated_data)