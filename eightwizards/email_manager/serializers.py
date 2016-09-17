from rest_framework import serializers


class EmailSerializer(serializers.Serializer):
    """
    Controls serialization of Skill model for REST API.
    """
    email = serializers.EmailField()
    name = serializers.CharField(max_length=125)
    message = serializers.CharField(max_length=2048)
