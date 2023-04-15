from rest_framework.generics import CreateAPIView

from .serializers import ThreadSerializer


class ThreadCreationView(CreateAPIView):
    serializer_class = ThreadSerializer


thread_creation = ThreadCreationView.as_view()
