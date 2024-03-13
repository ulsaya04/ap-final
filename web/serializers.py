from rest_framework import serializers

class text_serializer(serializers.Serializer):
    text = serializers.CharField()

class speech_serializer(serializers.Serializer):
    speech = serializers.FileField()