import json
import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .serializers import EmailSerializer


logger = logging.getLogger(__name__)


class EmailAPIViewSet(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin):
    """
    ReadOnly View set to provide public API for the ConfigParam.
    Writable operation will be allowed just for tuning machine
    """
    serializer_class = EmailSerializer

    def create(self, request, *args, **kwargs):
        serializier = self.serializer_class(data=request.data)
        if not serializier.is_valid():
            logger.error(serializier.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializier.errors)

        headers = {'X-SMTPAPI': json.dumps({'category': 'ses-emails'})}

        subject = 'Ping. You have message from {}'.format(serializier.data.get('name'))
        recipient_email = '{} <{}>'.format(serializier.data.get('name'), serializier.data.get('email'))
        if not recipient_email:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializier.errors)

        text_content = serializier.data.get('message')

        msg = EmailMultiAlternatives(subject, text_content, recipient_email,
                                     [getattr(settings, 'EMAIL_SENDER', None)], headers=headers)

        res = msg.send()

        return Response(res)
