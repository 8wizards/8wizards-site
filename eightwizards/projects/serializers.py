from rest_framework import serializers
from .models import Skill, Project, MediaResource


class SkillSerializer(serializers.ModelSerializer):
    """
    Controls serialization of Skill model for REST API.
    """
    class Meta:
        model = Skill


class ProjectSerializer(serializers.ModelSerializer):
    """
    Controls serialization of Project model for REST API.
    """
    class Meta:
        model = Project


class MediaSerializer(serializers.ModelSerializer):
    """
    Controls serialization of Media model for REST API.
    """
    class Meta:
        model = MediaResource
