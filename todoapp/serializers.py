from rest_framework import serializers

from todoapp.models import User, Item


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
    items = ItemSerializer(many=True, read_only=True)



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

        user = User.objects.filter(email=data['email']).first()
        if player:
            raise serializers.ValidationError(
                'USer with this email already exists.')
        return data


class UpdateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        required=True, allow_blank=False, max_length=150)
    last_name = serializers.CharField(
        required=True, allow_blank=False, max_length=150)
    email = serializers.EmailField(
        required=True, allow_blank=False)
    is_superuser = serializers.BooleanField(default=False)
    is_staff = serializers.BooleanField(default=False)
    is_active = serializers.BooleanField(default=False)

    def validate(self, data):
        player = Player.objects.filter(email=data['email']).first()
        if player and player.id != self.instance.id:
            raise serializers.ValidationError(
                'Player with this email already exists.')
        return data