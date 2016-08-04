import logging
from django.contrib import admin
from django.forms import ModelForm
from .models import Article


logger = logging.getLogger(__name__)


class ArticleForm(ModelForm):
    """
    The ModelForm class that encapsulates the configuration params data mapping to the Django model: Article
    """
    class Meta(object):
        model = Article
        fields = '__all__'


@admin.register(Article)
class ConfigParamAdmin(admin.ModelAdmin):
    """
    The HistoryModelAdmin for ConfigParam Model, provides views of the history of the ConfigParam model
    """
    form = ArticleForm
    list_display = ('title', 'published_at', 'is_visible')
    list_filter = ('is_visible',)

