from rest_framework import serializers
from .models import Skill, Project, MediaResource, Technology, Category
from team.serializers import MemberSerializer

class CategorySerializer(serializers.ModelSerializer):
    """
    Controls serialization of Skill model for REST API.
    """
    class Meta:
        model = Category

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
    technologies = TechnologySerializer(many=True, read_only=True)
    members = MemberSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Project


class MediaSerializer(serializers.ModelSerializer):
    """
    Controls serialization of Media model for REST API.
    """
    class Meta:
        model = MediaResource
