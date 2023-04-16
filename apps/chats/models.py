from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models


class Thread(models.Model):
    """
    Represents a chat with messages.

    Can contain only 2 participants.
    """

    participants = models.ManyToManyField(
        AUTH_USER_MODEL,
        related_name='threads',
        verbose_name='Owners of a thread',
    )
    created = models.DateTimeField(
        'Thread creation date and time', auto_now_add=True
    )
    updated = models.DateTimeField(
        'Thread last update date and time', auto_now_add=True
    )

    class Meta:
        db_table = 'thread'

    def __str__(self) -> str:
        return f'Thread: {self.id}'


class Message(models.Model):
    """
    Message in a thread.
    """

    sender = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='User that sent this message',
    )
    text = models.TextField('Message text', max_length=4096)
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Thread a message belongs to',
    )
    created = models.DateTimeField(
        'Message creation date and time', auto_now_add=True
    )
    is_read = models.BooleanField(
        'Message is read by all participants of a thread', default=False
    )

    class Meta:
        db_table = 'message'
        ordering = ('-created',)

    def __str__(self) -> str:
        return f'Sent by {self.sender}'
