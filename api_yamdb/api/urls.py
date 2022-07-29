from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, CreateUserView,
                    GenreViewSet, ReviewsViewSet, TitleViewSet, UserViewSet,
                    get_user_token)

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('genres', GenreViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/token/', get_user_token, name='token_obtain'),
    path('v1/auth/signup/', CreateUserView.as_view()),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
    path(
        'v1/users/me/',
        UserViewSet.as_view({'get': 'me', 'patch': 'me', 'delete': 'me'}),
        name='me',
    ),
    path('v1/', include(router_v1.urls)),
]
