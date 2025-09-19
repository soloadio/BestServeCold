from rest_framework import serializers

class RequestSerializer(serializers.Serializer):
  file = serializers.FileField()
  name = serializers.CharField(max_length=100)
  prompt = serializers.CharField(max_length=500)