import logging
from django.db import models
from django.conf import settings
from common.constants.models import ACTIVE, ACTIVE_INACTIVE_CHOICES


logger = logging.getLogger(__name__)


class ConfigParam(models.Model):

    name = models.CharField(max_length=64, db_index=True, unique=True)
    value = models.TextField()
    notes = models.TextField(null=True, blank=True)
    status = models.BooleanField(choices=ACTIVE_INACTIVE_CHOICES, default=ACTIVE, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name='Updated At')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_by_config_param', null=True,
                                   blank=True, on_delete=models.SET_NULL, verbose_name='Created By', editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='edited_by_config_param', null=True,
                                   blank=True, on_delete=models.SET_NULL, verbose_name='Updated By', editable=False)

    def __str__(self):
        return self.name

    class Meta(object):
        ordering = ('-updated_at',)
        verbose_name = 'Config Param'
        index_together = (('name', 'status'),)

    class HistoryMeta(object):
        fields = ('id_display', 'version_display', 'name', 'value', 'notes', 'status')

    def value_display(self):
        if str(self.value).__len__() > 36:
            return self.value[:32] + '...'
        return self.value
    value_display.short_description = 'Value'

    @staticmethod
    def get_param(name, default):
        try:
            obj = ConfigParam.objects.get(name=name, status=True)
            return obj.value
        except models.ObjectDoesNotExist:
            return default