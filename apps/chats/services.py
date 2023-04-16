from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch, QuerySet, Q

from .models import Thread, Message

User = get_user_model()


def get_thread_by_participants(participants: list[int]) -> Thread:
    """
    Return `Thread` object by m2m field `participants`.
    """
    users = User.objects.only('id')
    prefetch = Prefetch('participants', queryset=users)
    threads = Thread.objects.prefetch_related(prefetch)
    threads = threads.filter(participants=participants[0])
    threads = threads.filter(participants=participants[1])
    return threads.distinct().get()


def create_thread(data: dict, participants: list[int] = None) -> Thread:
    thread = Thread.objects.create(**data)
    if participants is not None:
        thread.participants.add(*participants)
    return thread


def get_by_participants_or_create_thread(
    data: dict, participants: list[int]
) -> tuple[Thread, bool]:
    """
    `get_or_create()` method but getting `Thread`
    object by m2m field `participants`.
    """
    try:
        return get_thread_by_participants(participants), False
    except ObjectDoesNotExist:
        return create_thread(data, participants), True


def set_thread_last_update(thread_id: int, created: datetime) -> None:
    """
    Update `updated` field of a `Thread` object.

    Is needed after creating new message in a thread.
    """
    Thread.objects.filter(id=thread_id).update(updated=created)


def mark_message_as_read(pk: int) -> None:
    Message.objects.filter(id=pk).update(is_read=True)


def get_unread_messages_number(user: User) -> QuerySet[Message]:
    """
    Get number of all unread messages of threads that the user have.
    """
    threads = Thread.objects.filter(participants=user)
    messages = Message.objects.select_related('sender', 'thread')
    return messages.filter(~Q(sender=user), is_read=False, thread__in=threads).count()


def check_user_have_thread(thread_pk: int, user: User):
    """
    Check whether user have a thread with a `thread_id`.
    """
    return user.threads.filter(id=thread_pk).exists()


def check_user_have_message(message_pk: int, user: User):
    """
    Check whether user has thread with the message.
    """
    return user.threads.filter(messages=message_pk)


def is_user_sender(message_pk: int, user: User) -> bool:
    """
    Check whether user is sender of the message.
    """
    return user.messages.filter(id=message_pk).exists()

