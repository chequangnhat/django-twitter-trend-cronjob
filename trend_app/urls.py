from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.urls import path
from .views import TestAPIView
from .views import NotAuthen
from .views import get_something
from .views import auth_get_data
from .views import get_user_id
from .views import add_favorite_trend
from .views import get_favorite_trend
from .views import get_current_trend

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('info/', TestAPIView.as_view()),
    path('notauth/', NotAuthen.as_view()),
    # path('get_something/<str:woeid>/', get_something),
    path('get_something/<str:woeid>/', get_current_trend),
    path('auth_get_data/<str:woeid>/', auth_get_data),
    path('get_user_id/', get_user_id),
    path('add_favorite_trend/', add_favorite_trend),
    path('get_favorite_trend/<str:user_id>/', get_favorite_trend),
]