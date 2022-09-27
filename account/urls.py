from django.urls import path

from account import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-create/', views.UserCreateView.as_view()),
    path('user-update/<int:id>/', views.UserUpdateView.as_view()),
]
