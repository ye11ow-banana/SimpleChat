from django.urls import path

from . import views

urlpatterns = [
    path('thread/create/', views.thread_creation),
    path('thread/<int:pk>/destroy/', views.thread_destroy),
    path('thread/list/', views.thread_list),
    path('thread/<int:thread_id>/message/create/', views.message_creation),
    path('thread/<int:thread_id>/message/list/', views.message_list),
    path('message/<int:pk>/read/', views.message_marking_as_read),
    path('message/number-unread/', views.unread_messages_number),
]
