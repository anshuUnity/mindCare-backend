from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    response = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.user.username} in conversation {self.conversation.id}"

