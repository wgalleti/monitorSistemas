from rest_framework import serializers
from .models import Lock


class LockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lock
        fields = '__all__'