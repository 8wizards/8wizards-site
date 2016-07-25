import logging
from django.contrib import admin
from django.forms import ModelForm
from .models import ConfigParam


logger = logging.getLogger(__name__)


class ConfigParamForm(ModelForm):
    """
    The ModelForm class that encapsulates the configuration params data mapping to the Django model: ConfigParam
    """
    class Meta(object):
        model = ConfigParam
        fields = '__all__'


@admin.register(ConfigParam)
class ConfigParamAdmin(admin.ModelAdmin):
    """
    The HistoryModelAdmin for ConfigParam Model, provides views of the history of the ConfigParam model
    """
    form = ConfigParamForm
    list_display = ('name', 'value', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)

