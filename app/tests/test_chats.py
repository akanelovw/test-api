import pytest
from rest_framework.test import APIClient

from chats.models import Chat, Message


@pytest.mark.django_db
class TestChatsAPI:

    def test_create_chat(self, client):
        """POST /chats/ → создаёт чат"""
        response = client.post("/chats/", {"title": "  Test Chat  "}, format="json")
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Chat"
        assert "id" in data
        assert "created_at" in data

    def test_create_chat_empty_title(self, client):
        """POST /chats/ с пустым title → 400"""
        response = client.post("/chats/", {"title": "   "}, format="json")
        assert response.status_code == 400
        
    def test_create_message(self, client):
        """POST /chats/<id>/messages/ → создаёт сообщение в чате"""
        chat = Chat.objects.create(title="Chat 1")
        response = client.post(f"/chats/{chat.id}/messages/", {"text": "  Test Text  "}, format="json")
        assert response.status_code == 201
        data = response.json()
        assert data["text"] == "Test Text"
        assert "id" in data

    def test_create_message_empty_text(self, client):
        """POST /chats/<id>/messages/ с пустым text → 400"""
        chat = Chat.objects.create(title="Chat 1")
        response = client.post(f"/chats/{chat.id}/messages/", {"text": "   "}, format="json")
        assert response.status_code == 400

    def test_create_message_nonexistent_chat(self, client):
        """POST в несуществующий чат → 404"""
        response = client.post("/chats/999/messages/", {"text": "Test Text"}, format="json")
        assert response.status_code == 404

    def test_get_chat_with_limit(self, client):
        """GET /chats/<id>?limit=N → возвращает последние N сообщений"""
        chat = Chat.objects.create(title="Test Chat")
        for i in range(5):
            Message.objects.create(chat=chat, text=f"msg {i}")

        response = client.get(f"/chats/{chat.id}/?limit=3")
        assert response.status_code == 200
        messages = response.json()["messages"]
        assert len(messages) == 3
        assert [m["text"] for m in messages] == ["msg 2", "msg 3", "msg 4"]

    def test_get_chat_limit_bounds(self, client):
        """Проверка граничных значений limit (min=1, max=100)"""
        chat = Chat.objects.create(title="Test Chat")
        for i in range(150):
            Message.objects.create(chat=chat, text=f"msg {i}")

        response = client.get(f"/chats/{chat.id}/?limit=0")
        assert len(response.json()["messages"]) == 1

        response = client.get(f"/chats/{chat.id}/?limit=200")
        assert len(response.json()["messages"]) == 100

    def test_delete_chat_cascade(self, client):
        """DELETE /chats/<id> → удаляет чат и все сообщения каскадно"""
        chat = Chat.objects.create(title="Test Chat")
        Message.objects.create(chat=chat, text="msg 1")
        Message.objects.create(chat=chat, text="msg 2")

        response = client.delete(f"/chats/{chat.id}/")
        assert response.status_code == 204
        assert Message.objects.filter(chat=chat).count() == 0
