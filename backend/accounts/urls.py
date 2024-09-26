from django.urls import path
from .views import (UserSignupView, UserLoginView, 
                    DummyView, UserProfileView, PasswordResetRequestView,
                    PasswordResetView, PasswordChangeView)

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('dummy/', DummyView.as_view(), name='dummy-view'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('password-reset/request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password-change/', PasswordChangeView.as_view(), name='password-change'),
]