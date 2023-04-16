from rest_framework.permissions import BasePermission

from . import services


class IsThreadParticipant(BasePermission):
    """
    Allows access only to participant users.
    """

    def has_permission(self, request, view):
        pk = view.kwargs['pk']
        user = request.user
        return services.check_user_have_thread(pk, user)


class IsThreadMessageParticipant(BasePermission):
    """
    Allows access only to participant of a thread that has the message.
    """

    def has_permission(self, request, view):
        pk = view.kwargs['pk']
        user = request.user
        return services.check_user_have_message(pk, user)


class IsNotSender(BasePermission):
    """
    Allows access only to user that is not sender of the message.
    """

    def has_permission(self, request, view):
        pk = view.kwargs['pk']
        user = request.user
        return not services.is_user_sender(pk, user)
