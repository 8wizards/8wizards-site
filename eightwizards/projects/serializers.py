from rest_framework import serializers
from .models import Skill, Project, MediaResource, Technology


class SkillSerializer(serializers.ModelSerializer):
    """
    Controls serialization of Skill model for REST API.
    """
    class Meta:
        model = Skill


class TechnologySerializer(serializers.ModelSerializer):
    """
    Controls serialization of Technology model for REST API.
    """
    class Meta:
        model = Technology


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
