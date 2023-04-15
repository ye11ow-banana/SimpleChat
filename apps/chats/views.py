from rest_framework.generics import CreateAPIView, DestroyAPIView

from .models import Thread
from .serializers import ThreadSerializer


class ThreadCreationView(CreateAPIView):
    serializer_class = ThreadSerializer


class ThreadDestroyView(DestroyAPIView):
    queryset = Thread.objects


thread_creation = ThreadCreationView.as_view()
thread_destroy = ThreadDestroyView.as_view()
