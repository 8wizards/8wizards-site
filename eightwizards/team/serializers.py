from rest_framework import serializers
from .models import Member, PromoUrl, Certification, Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role


class MemberSerializer(serializers.ModelSerializer):
    """
    Controls serialization of Member model for REST API.
    """
    role = RoleSerializer(read_only=True)

    class Meta:
        model = Member



class PromoUrlSerializer(serializers.ModelSerializer):
    """
    Controls serialization of PromoUrl model for REST API.
    """
    class Meta:
        model = PromoUrl


class CertificationSerializer(serializers.ModelSerializer):
    """
    Controls serialization of Certification model for REST API.
    """
    class Meta:
        model = Certification
