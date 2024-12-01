# chat/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Message
from .serializers import MessageSerializer
from .utils import get_openai_response, CHAT_PROMPT
import openai
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

class ChatBotView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        content = request.data.get('content', '')

        if not content:
            return Response({"error": "Message content is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the last 10 messages for the user
        last_messages = Message.objects.filter(user=user).order_by('-timestamp')[:10]

        # Construct OpenAI messages format
        messages = [{"role": "system", "content": CHAT_PROMPT}]
        for msg in reversed(last_messages):  # Reverse to maintain chronological order
            messages.append({"role": "user", "content": msg.content})
            if msg.response:
                messages.append({"role": "assistant", "content": msg.response})

        # Add the new user message to the context
        messages.append({"role": "user", "content": content})

        # Save the user message
        user_message = Message.objects.create(user=user, content=content)

        try:
            # Call the utility function to get the OpenAI response
            bot_response = get_openai_response(messages)

            # Save bot response
            user_message.response = bot_response
            user_message.save()

            # Serialize and return the response
            serializer = MessageSerializer(user_message)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except openai.error.OpenAIError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChatHistoryPagination(PageNumberPagination):
    page_size = 10  # Number of messages per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserChatHistoryView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    pagination_class = ChatHistoryPagination

    def get_queryset(self):
        """
        Fetch chat history for the authenticated user.
        """
        return Message.objects.filter(user=self.request.user).order_by('-timestamp')