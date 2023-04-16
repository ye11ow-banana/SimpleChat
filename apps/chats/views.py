from requests import Request
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from django.db.models import QuerySet

from . import services
from .models import Thread, Message
from . import permissions
from .serializers import ThreadSerializer, MessageSerializer


class ThreadCreationView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ThreadSerializer


class ThreadDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, permissions.IsThreadParticipant]
    queryset = Thread.objects


class ThreadListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ThreadSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self) -> QuerySet[Thread]:
        user = self.request.user
        return Thread.objects.filter(participants=user)


class MessageCreationView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, permissions.IsThreadParticipant]
    serializer_class = MessageSerializer

    def perform_create(self, serializer: MessageSerializer) -> None:
        thread_id = self.kwargs['pk']
        threads = Thread.objects.filter(id=thread_id)
        thread = get_object_or_404(threads)
        user = self.request.user
        serializer.save(thread=thread, sender=user)


class MessageListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, permissions.IsThreadParticipant]
    serializer_class = MessageSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self) -> QuerySet[Message]:
        thread_id = self.kwargs['pk']
        return Message.objects.filter(thread_id=thread_id)


class MessageMarkingAsReadView(APIView):
    """
    View for updating `is_read` field of a `Message` object.
    """
    permission_classes = [
        IsAuthenticated,
        permissions.IsThreadMessageParticipant,
        permissions.IsNotSender,
    ]

    def patch(self, request: Request, pk: int) -> Response:
        services.mark_message_as_read(pk)
        return Response(status=HTTP_200_OK)


class UnreadMessagesNumberView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        number = services.get_unread_messages_number(self.request.user)
        return Response(number, status=HTTP_200_OK)


thread_creation = ThreadCreationView.as_view()
thread_destroy = ThreadDestroyView.as_view()
thread_list = ThreadListView.as_view()
message_creation = MessageCreationView.as_view()
message_list = MessageListView.as_view()
message_marking_as_read = MessageMarkingAsReadView.as_view()
unread_messages_number = UnreadMessagesNumberView.as_view()
