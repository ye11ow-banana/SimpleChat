from django.contrib.auth import get_user_model
from rest_framework import serializers

from . import services
from .models import Thread, Message

User = get_user_model()


class ThreadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thread
        fields = '__all__'
        read_only_fields = ('created', 'updated')

    def validate_participants(self, value: list[int]) -> list[int]:
        """
        Check that a thread can have only 2 participants.
        """
        if len(value) != 2:
            raise serializers.ValidationError(
                'Thread needs to have 2 participants')
        return value

    def to_representation(self, data):
        participants = [
            {'id': obj.id, 'username': obj.username}
            for obj in data.participants.all()
        ]
        representation = super().to_representation(data)
        representation['participants'] = participants
        return representation

    def to_internal_value(self, data: dict) -> dict:
        participants = data['participants']
        validated_data = super().to_internal_value(data)
        validated_data['participants'] = participants
        return validated_data

    def create(self, validated_data: dict) -> Thread:
        participants = validated_data.pop('participants')
        thread, _ = services.get_by_participants_or_create_thread(
            validated_data, participants
        )
        return thread


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    thread = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('created', 'is_read')
