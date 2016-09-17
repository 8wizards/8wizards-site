from rest_framework import viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin
from common.constants.models import ACTIVE
from .serializers import SkillSerializer, ProjectSerializer, MediaSerializer, TechnologySerializer, CategorySerializer
from .models import Skill, Project, MediaResource, Technology, Category


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly View set to provide public API for the Category.
    Writable operation will be allowed just for tuning machine
    """

    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly View set to provide public API for the Skill.
    Writable operation will be allowed just for tuning machine
    """

    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class TechnologyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly View set to provide public API for the Technology.
    Writable operation will be allowed just for tuning machine
    """

    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer


class ProjectViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly View set to provide public API for the Project.
    Writable operation will be allowed just for tuning machine
    """

    queryset = Project.objects.filter(status=ACTIVE)
    serializer_class = ProjectSerializer


class MediaViewSet(viewsets.mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    ReadOnly View set to provide public API for the Media.
    Writable operation will be allowed just for tuning machine
    """

    queryset = MediaResource.objects.all()
    serializer_class = MediaSerializer
