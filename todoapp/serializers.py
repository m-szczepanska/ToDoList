from rest_framework import serializers

from todoapp.models import User, Item
from todoapp.services import (
    MinimumLengthValidator, NumericPasswordValidator)


class ItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title=serializers.CharField(
        max_length=200, required=True, allow_blank=False)
    text = serializers.CharField(allow_blank=True)
    status = serializers.ChoiceField(
        choices=Item.STATUS_CHOICES,required=True,
        allow_blank=False)
    category = serializers.ChoiceField(
        choices=Item.CATEGORY_CHOICES,required=True,
        allow_blank=False)
    due_date = serializers.DateTimeField(required=False)
    created_at = serializers.DateTimeField(required=False)
    creator_id = serializers.IntegerField(required=False)
    owner_id = serializers.IntegerField(required=False)


class GetUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(
        required=True, allow_blank=False, max_length=150)
    last_name = serializers.CharField(
        required=True, allow_blank=False, max_length=150)
    email = serializers.EmailField(
        required=True, allow_blank=False)
    username = serializers.CharField(
        required=True, allow_blank=False, max_length=150)
    owned_items = ItemSerializer(many=True, read_only=True)


class CreateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        required=True, allow_blank=False, max_length=150)
    last_name = serializers.CharField(
        required=True, allow_blank=False, max_length=150)
    email = serializers.EmailField(
        required=True, allow_blank=False)
    username = serializers.CharField(
        required=True, allow_blank=False, max_length=150)
    password = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    password_repeat = serializers.CharField(
        required=True, allow_blank=False, max_length=255)

    def validate(self, data):
        if data['password'] != data['password_repeat']:
            raise serializers.ValidationError('Passwords did not match.')
        elif not MinimumLengthValidator.validate(data['password']):
            raise serializers.ValidationError(
                'Passwords must have at least 8 characters')
        elif not NumericPasswordValidator.validate(data['password']):
            raise serializers.ValidationError(
                'Password must contain at least 1 digit')

        user_mail = User.objects.filter(email=data['email']).first()
        user_name = User.objects.filter(username=data['username']).first()
        if user_mail:
            raise serializers.ValidationError(
                'User with this email already exists.')
        elif user_name:
            raise serializers.ValidationError(
                'User with this username already exists.')
        return data


class UpdateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        required=True, allow_blank=False, max_length=150)
    last_name = serializers.CharField(
        required=True, allow_blank=False, max_length=150)
    email = serializers.EmailField(
        required=True, allow_blank=False)

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if user and user.id != self.instance.id:
            raise serializers.ValidationError(
                'User with this email already exists.')
        return data