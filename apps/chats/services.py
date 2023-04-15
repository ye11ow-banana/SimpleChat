from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch

from .models import Thread

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
