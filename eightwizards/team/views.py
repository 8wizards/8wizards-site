from rest_framework import viewsets
from .serializers import MemberSerializer, PromoUrlSerializer, CertificationSerializer
from common.constants.models import ACTIVE
from .models import Member, PromoUrl, Certification


class MemberViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly View set to provide public API for the Member.
    Writable operation will be allowed just for tuning machine
    """

    queryset = Member.objects.filter(status=ACTIVE)
    serializer_class = MemberSerializer


class PromoUrlViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly View set to provide public API for the PromoUrl.
    Writable operation will be allowed just for tuning machine
    """

    queryset = PromoUrl.objects.all()
    serializer_class = PromoUrlSerializer


class CertificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly View set to provide public API for the Media.
    Writable operation will be allowed just for tuning machine
    """

    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
