import random

from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CONFIRMATION_CODE_LENGTH
from users.permissions import AdminOnly
from users.serializers import (GetTokenSerializer, NotAdminSerializer,
                               SignUpSerializer, UserSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly, IsAuthenticated)
    http_method_names = ['get', 'post', 'patch', 'delete']
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me'
    )
    def get_user_info(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UserSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class GetTokenView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user_instance = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user_instance.confirmation_code:
            token = RefreshToken.for_user(user_instance).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_200_OK)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def send_email(data):
        """Отправь email."""
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    @staticmethod
    def generate_confirmation_code() -> str:
        """Сгенерируй код подтверждения."""
        digs = '1234567890'
        code = ''
        for _ in range(CONFIRMATION_CODE_LENGTH):
            code += random.choice(digs)
        return code

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_instance = User.objects.get_or_create(
            **serializer.validated_data)[0]
        validated_username = serializer.validated_data['username']
        User.objects.filter(
            username=validated_username).update(
            confirmation_code=self.generate_confirmation_code())

        email_body = (
            f'Привет, {user_instance.username}! '
            f'Ваш код подтвержения: {user_instance.confirmation_code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user_instance.email,
            'email_subject': 'Код подтвержения для доступа к YamDB.'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
