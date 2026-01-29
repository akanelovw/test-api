from django.urls import path
from .views import ChatCreateView, ChatDetailView, MessageCreateView

urlpatterns = [
    path("", ChatCreateView.as_view()),
    path("<int:pk>/", ChatDetailView.as_view()),
    path("<int:pk>/messages/", MessageCreateView.as_view()),
]