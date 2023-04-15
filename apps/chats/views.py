from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView

from .models import Thread
from .serializers import ThreadSerializer


class ThreadCreationView(CreateAPIView):
    serializer_class = ThreadSerializer


class ThreadDestroyView(DestroyAPIView):
    queryset = Thread.objects


class ThreadListView(ListAPIView):
    serializer_class = ThreadSerializer

    def get_queryset(self):
        user = self.request.user
        return Thread.objects.filter(participants=user)


thread_creation = ThreadCreationView.as_view()
thread_destroy = ThreadDestroyView.as_view()
thread_list = ThreadListView.as_view()
