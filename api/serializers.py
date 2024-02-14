from rest_framework import serializers
from .models import MessageTo

class PenziMessageSerializer(serializers.Serializer):
    msisdn = serializers.CharField(max_length=15)
    short_code = serializers.CharField(max_length=6)
    message_content = serializers.CharField()

    def create(self, validated_data):
        message_to = MessageTo.objects.create(short_code=validated_data['short_code'])
        return message_to
