import re

from rest_framework import serializers


class ValidateUsernameMixin:

    def validate_username(self, value):
        if not re.search(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                'Введите корректное имя пользователя.')
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.')
        return value
