from django.urls import path
from .views import ChatBotView, UserChatHistoryView

urlpatterns = [
    path("chat/", ChatBotView.as_view(), name="chat"),
    path("chat/history/", UserChatHistoryView.as_view(), name="chat-history")
]