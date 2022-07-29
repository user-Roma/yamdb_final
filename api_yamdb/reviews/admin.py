from django.contrib import admin
from import_export import resources, widgets
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from .models import Category, Comment, Genre, GenreTitle, Review, Title, User


class UserResource(resources.ModelResource):

    class Meta:
        model = User


class CategoriesResource(resources.ModelResource):

    class Meta:
        model = Category


class CommentsResource(resources.ModelResource):
    pub_date = Field(
        attribute='pub_date',
        column_name='pub_date',
        widget=widgets.DateTimeWidget('%Y-%m-%dT%H:%M:%S.%fZ'))

    class Meta:
        model = Comment


class GenreTitleResource(resources.ModelResource):

    class Meta:
        model = GenreTitle


class GenreResource(resources.ModelResource):

    class Meta:
        model = Genre


class ReviewsResource(resources.ModelResource):
    pub_date = Field(
        attribute='pub_date',
        column_name='pub_date',
        widget=widgets.DateTimeWidget('%Y-%m-%dT%H:%M:%S.%fZ'))

    class Meta:
        model = Review


class TitleResource(resources.ModelResource):

    class Meta:
        model = Title


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource
    list_display = (
        'username',
        'pk',
        'first_name',
        'last_name',
        'is_active',
        'role',
        'is_staff',
        'last_login',
    )
    list_editable = ('role', 'is_active',)
    list_filter = ('role', 'is_active',)


@admin.register(Category)
class CategoriesAdmin(ImportExportModelAdmin):
    resource_class = CategoriesResource


@admin.register(Comment)
class CommentsAdmin(ImportExportModelAdmin):
    resource_class = CommentsResource


@admin.register(GenreTitle)
class GenreTitleAdmin(ImportExportModelAdmin):
    resource_class = GenreTitleResource


@admin.register(Genre)
class GenreAdmin(ImportExportModelAdmin):
    resource_class = GenreResource


@admin.register(Review)
class ReviewsAdmin(ImportExportModelAdmin):
    resource_class = ReviewsResource


@admin.register(Title)
class TitleAdmin(ImportExportModelAdmin):
    resource_class = TitleResource
