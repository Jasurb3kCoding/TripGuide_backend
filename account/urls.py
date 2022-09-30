from django.urls import path

from account import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', views.UserCreateView.as_view()),
    path('users/<int:id>/', views.UserUpdateView.as_view()),
    path('user-settings/<int:id>/', views.UserSettingUpdateView.as_view()),
    path('languages/', views.LanguageListView.as_view()),
    path('user-verify/', views.user_verify),

]
