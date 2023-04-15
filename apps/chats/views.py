from requests import Request
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from . import services
from .models import Thread, Message
from .serializers import ThreadSerializer, MessageSerializer


class ThreadCreationView(generics.CreateAPIView):
    serializer_class = ThreadSerializer


class ThreadDestroyView(generics.DestroyAPIView):
    queryset = Thread.objects


class ThreadListView(generics.ListAPIView):
    serializer_class = ThreadSerializer

    def get_queryset(self):
        user = self.request.user
        return Thread.objects.filter(participants=user)


class MessageCreationView(generics.CreateAPIView):
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        thread_id = self.kwargs['thread_id']
        threads = Thread.objects.filter(id=thread_id)
        thread = get_object_or_404(threads)
        user = self.request.user
        serializer.save(thread=thread, sender=user)


class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        thread_id = self.kwargs['thread_id']
        return Message.objects.filter(thread_id=thread_id)


class MessageMarkingAsReadView(APIView):
    """
    View for updating `is_read` field of a `Message` object.
    """

    def patch(self, request: Request, pk: int) -> Response:
        services.mark_message_as_read(pk)
        return Response(status=HTTP_200_OK)


thread_creation = ThreadCreationView.as_view()
thread_destroy = ThreadDestroyView.as_view()
thread_list = ThreadListView.as_view()
message_creation = MessageCreationView.as_view()
message_list = MessageListView.as_view()
message_marking_as_read = MessageMarkingAsReadView.as_view()
