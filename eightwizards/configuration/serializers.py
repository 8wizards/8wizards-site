from rest_framework import serializers
from .models import ConfigParam


class ConfigParamSerializer(serializers.ModelSerializer):
    """
    Controls serialization of ConfigParam model for REST API.
    """
    class Meta:
        model = ConfigParam
