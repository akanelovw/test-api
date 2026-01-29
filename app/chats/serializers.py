from rest_framework import serializers
from .models import Chat, Message

DEFAULT_LIMIT: int = 20
MIN_LIMIT: int = 1
MAX_LIMIT: int = 100

class MessageSerializer(serializers.ModelSerializer[Message]):
    class Meta:
        model = Message
        fields = ("id", "text", "created_at")

    def validate_text(self, value: str) -> str:
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Text cannot be empty")

        return value


class ChatSerializer(serializers.ModelSerializer[Chat]):
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ("id", "title", "created_at", "messages")

    def validate_title(self, value: str) -> str:
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Title cannot be empty")

        return value

    def get_messages(self, obj: Chat) -> list[dict]:
        request = self.context.get("request")

        limit = request.query_params.get("limit", DEFAULT_LIMIT)

        try:
            limit = int(limit)
        except ValueError:
            limit = DEFAULT_LIMIT

        limit = max(MIN_LIMIT, min(limit, MAX_LIMIT))

        messages = obj.messages.order_by("-created_at")[:limit]

        return MessageSerializer(
            list(messages)[::-1],
            many=True
        ).data