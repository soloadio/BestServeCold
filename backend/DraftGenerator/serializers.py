from rest_framework import serializers

class RequestSerializer(serializers.Serializer):
  unique_id = serializers.CharField(max_length=100)
  name = serializers.CharField(max_length=100)
  university = serializers.CharField(max_length=100)
  program = serializers.CharField(max_length=100)
  file = serializers.FileField()
  prompt = serializers.CharField(max_length=500, required=False, allow_blank=True)

from rest_framework import serializers
from .models import Draft, Batch
from User.models import User

# Serializer for Draft
class DraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = '__all__'


# Serializer for Batch
class BatchSerializer(serializers.ModelSerializer):
    drafts = DraftSerializer(many=True, read_only=True)
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = Batch
        fields = '__all__'