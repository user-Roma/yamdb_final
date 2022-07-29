import uuid

from core.validators import year_validator
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title, User

ERRORS = {
    'user_exists': 'Пользователь с таким email уже есть',
    'field_required': 'Обязательное поле',
    'me_restrict': 'Логин "me" нельзя использовать',
}


class CustomUserSerializer(UserCreateSerializer):
    """Custom user serializer."""

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')
        if User.objects.filter(email=email).first():
            raise serializers.ValidationError(
                {"email": ERRORS.get('user_exists')}
            )
        if username == 'me':
            raise serializers.ValidationError(
                {"username": ERRORS.get('me_restrict')}
            )
        if attrs.get('role') in dict(User.USER_ROLES):
            attrs['role'] = (
                dict(User.USER_ROLES).get(attrs.get('role'))
                or User.USER)
        return attrs


class SelfRegisterSerializer(CustomUserSerializer):
    """User self-registration serializer."""

    def create(self, validated_data):
        confirm_code = uuid.uuid4().hex[:8]
        email = validated_data.get('email')
        username = validated_data.get('username')
        send_mail(
            settings.EMAIL_CONFIG.get('subject'),
            settings.EMAIL_CONFIG.get('text').format(username, confirm_code),
            settings.EMAIL_CONFIG.get('from'),
            [email],
            fail_silently=False,
        )
        return User.objects.create_user(
            username=username,
            email=email,
            confirm_code=confirm_code,
            is_active=False,
        )

    class Meta:
        model = User
        fields = ('username', 'email',)


class UserSerializer(CustomUserSerializer):
    """Serializer for users."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class MeSerializer(CustomUserSerializer):
    """Serializer for my User."""

    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for genres."""

    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for categories."""

    class Meta:
        model = Category
        exclude = ('id',)


class TitleReadSerializer(serializers.ModelSerializer):
    """Serializer for list and retieve methods with titles."""

    category = CategorySerializer()
    genre = GenreSerializer(many=True,)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = ('__all__')
        read_only_fields = ('category', 'genre', 'rating',)


class TitleWriteSerializer(serializers.ModelSerializer):
    """Serializer for not safe methods with titles."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug')
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True)

    class Meta:
        model = Title
        fields = ('__all__')

    def validate_year(self, value):
        return year_validator(value)


class ReviewsSerializer(serializers.ModelSerializer):
    """Serializer for reviews."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        exclude = ('title',)
        model = Review

    def validate(self, data):
        title_id = self.context.get(
            'request'
        ).parser_context.get('kwargs').get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        author = self.context['request'].user
        if self.context['request'].method == 'POST':
            if author.reviews.filter(title_id=title).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили отзыв на это произведение!'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        exclude = ('review', )
        model = Comment
