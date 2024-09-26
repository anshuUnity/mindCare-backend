from django.urls import path
from .views import UserSignupView, UserLoginView, DummyView, UserProfileView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('dummy/', DummyView.as_view(), name='dummy-view'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]