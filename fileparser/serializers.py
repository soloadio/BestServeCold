from rest_framework import serializers

class RequestSerializer(serializers.Serializer):
  name = serializers.CharField(max_length=100)
  university = serializers.CharField(max_length=100)
  program = serializers.CharField(max_length=100)
  file = serializers.FileField()
  prompt = serializers.CharField(max_length=500,
                                 required=False,
                                 allow_blank=True)