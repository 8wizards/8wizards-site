from rest_framework import viewsets
from .serializers import SkillSerializer, ProjectSerializer, MediaSerializer
from .models import Skill, Project, MediaResource


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly View set to provide public API for the Skill.
    Writable operation will be allowed just for tuning machine
    """

    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly View set to provide public API for the Project.
    Writable operation will be allowed just for tuning machine
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class MediaViewSet(viewsets.mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    ReadOnly View set to provide public API for the Media.
    Writable operation will be allowed just for tuning machine
    """

    queryset = MediaResource.objects.all()
    serializer_class = MediaSerializer
