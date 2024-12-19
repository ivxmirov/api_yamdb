from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from users.mixins import ValidateUsernameMixin

User = get_user_model()


class UserSerializer(serializers.ModelSerializer, ValidateUsernameMixin):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class NotAdminSerializer(serializers.ModelSerializer, ValidateUsernameMixin):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


class GetTokenSerializer(serializers.ModelSerializer, ValidateUsernameMixin):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class SignUpSerializer(serializers.Serializer, ValidateUsernameMixin):
    username = serializers.CharField(
        validators=(UnicodeUsernameValidator(),),
        max_length=150,
    )
    email = serializers.EmailField(max_length=254)

    def validate(self, data):
        if User.objects.filter(
                email=data['email'], username=data['username']).first():
            return (data)
        elif (User.objects.filter(email=data['email']).first()
                and User.objects.filter(username=data['username']).first()):
            raise serializers.ValidationError(
                {
                    'username': 'Такой username уже используется.',
                    'email': 'Такой email уже используется.'
                }
            )
        elif User.objects.filter(email=data['email']).first():
            raise serializers.ValidationError(
                {'email': 'Такой email уже используется.'}
            )
        elif User.objects.filter(username=data['username']).first():
            raise serializers.ValidationError(
                {'username': 'Такой username уже используется.'}
            )
        return data
