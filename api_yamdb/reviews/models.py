from core.validators import year_validator
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    """User model."""
    ADMIN = 'admin'
    USER = 'user'
    MODERATOR = 'moderator'
    USER_ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль', choices=USER_ROLES, max_length=9, default=USER)
    confirm_code = models.CharField(
        'Код подтверждения', null=True, max_length=8)
    email = models.EmailField(
        'Адрес эл. почты', unique=True, null=False)

    class Meta:

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return (f'[User {self.id}]-  {self.last_name} {self.email}')


class Category(models.Model):
    """Model: categories (types) of works ("Films", "Books", "Music")."""

    name = models.CharField('Вид категории', max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:

        ordering = ('slug',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return (f'[Category {self.id}] [Slug {self.slug}]-  {self.name}')


class Genre(models.Model):
    """Model: genres of works. One work can be tied to several genres."""

    name = models.CharField('Жанр произведения', max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return (f'[Genre {self.id}] [Slug {self.slug}]-  {self.name}')


class Title(models.Model):
    """Model: name of work for which reviews are written."""

    name = models.TextField('Название произведения')
    year = models.IntegerField('Год выпуска', validators=[year_validator])
    description = models.TextField('Описание', blank=True, null=True)
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', verbose_name='Жанр')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles',
        blank=True, null=True, verbose_name='Категория')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Название'
        verbose_name_plural = 'Названия'

    def __str__(self):
        return (
            f'[Title {self.id}]'
            f'[Category {self.category}]'
            f'-  {self.year} {self.name}'
        )


class GenreTitle(models.Model):
    """Model: connections titles with genres."""

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta:

        verbose_name = 'Жанр - Название произведения'
        verbose_name_plural = 'Жанры - Названия произведений'

    def __str__(self):
        return (
            f'[Pair {self.id}]: [Genre {self.genre}] '
            f'- [Title {self.title}]'
        )


class Review(models.Model):
    """Model: reviews of works. Review is tied to a specific product."""

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(
        'Оценка произведения',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ])
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title_id', 'author'],
                name='unique_review'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']

    def __str__(self):
        return (
            f'[Review {self.id}] [Title {self.title.id}]'
            f'-  {self.pub_date} {self.author} '
            f'{self.text[:15]} {self.score}'
        )


class Comment(models.Model):
    """Model: comments on reviews. Comment is tied to a specific review."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField('Комментарий')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:

        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return (
            f'[Comment {self.id}] [Review {self.review.id}]'
            f'-  {self.pub_date} {self.author} '
            f'{self.text[:15]}'
        )
