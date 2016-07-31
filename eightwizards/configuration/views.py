# from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ConfigParamSerializer
from .models import ConfigParam


class ConfigParamViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly View set to provide public API for the ConfigParam.
    Writable operation will be allowed just for tuning machine
    """

    queryset = ConfigParam.objects.all()
    serializer_class = ConfigParamSerializer
