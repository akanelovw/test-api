from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView
from django.shortcuts import get_object_or_404

from .models import Chat
from .serializers import ChatSerializer, MessageSerializer


# POST /chats/
class ChatCreateView(CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


# GET + DELETE /chats/{id}/
class ChatDetailView(RetrieveDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


# POST /chats/{id}/messages/
class MessageCreateView(CreateAPIView):
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        chat = get_object_or_404(Chat, pk=self.kwargs["pk"])
        serializer.save(chat=chat)