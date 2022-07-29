from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken

from core.api_views import RetrieveUpdateModelMixin
from core.filters import TitleFilters
from core.permissions import (AdminOnly, AdminOrReadOnly,
                              AuthorAdminModerOrReadOnly)
from reviews.models import Category, Comment, Genre, Review, Title, User

from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, MeSerializer, ReviewsSerializer,
                          SelfRegisterSerializer, TitleReadSerializer,
                          TitleWriteSerializer, UserSerializer)


class CreateUserView(CreateAPIView):
    """User self-registration view (create only)."""
    model = User
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = SelfRegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes((permissions.AllowAny, ))
def get_user_token(request):
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')
    if username is None:
        return Response(
            {'username': 'Обязательное поле'}, status.HTTP_400_BAD_REQUEST
        )
    if confirmation_code is None:
        return Response(
            {'confirmation_code': 'Обязательное поле'},
            status.HTTP_400_BAD_REQUEST
        )
    user = User.objects.filter(username=username).first()
    if user:
        user_code = user.confirm_code
        if user_code == confirmation_code and not user.is_active:
            user.is_active = True
            user.save()
            token = str(SlidingToken.for_user(user))
            token = str(
                RefreshToken.for_user(user).access_token
            )
            return Response({'token': token}, status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Неверный код подтверждения'},
                status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {'error': 'Пользователь не найден'},
            status.HTTP_404_NOT_FOUND
        )


class UserViewSet(viewsets.ModelViewSet):
    """Viewset for users."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    lookup_field = 'username'

    def get_permissions(self):
        if self.action == 'me':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [AdminOnly]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['patch', 'get', 'delete'])
    def me(self, request, pk=None):
        if request.method == 'DELETE':
            return Response(
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        user = self.request.user
        serializer = MeSerializer(user)
        if request.method == 'PATCH':
            serializer = MeSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
        return Response(serializer.data)


class GenreViewSet(RetrieveUpdateModelMixin):
    """Viewset for genres."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(RetrieveUpdateModelMixin):
    """Viewset for categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Viewset for titles."""

    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = [AdminOrReadOnly]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filterset_class = TitleFilters

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    """Viewset for reviews."""

    serializer_class = ReviewsSerializer
    permission_classes = [AuthorAdminModerOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(
            Title, id=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Viewset for comments."""

    serializer_class = CommentSerializer
    permission_classes = [AuthorAdminModerOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(
            Review, id=self.kwargs.get('review_id')
        )
        return Comment.objects.filter(
            review=review
        )

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(
            author=self.request.user,
            review=review
        )
