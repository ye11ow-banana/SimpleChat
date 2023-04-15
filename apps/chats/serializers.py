from rest_framework import serializers

from . import services
from .models import Thread


class ThreadSerializer(serializers.ModelSerializer):
    participants = serializers.StringRelatedField(many=True)

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

    def to_internal_value(self, data: dict) -> dict:
        return data

    def create(self, validated_data: dict) -> Thread:
        participants = validated_data.pop('participants')
        thread, _ = services.get_by_participants_or_create_thread(
            validated_data, participants
        )
        return thread
