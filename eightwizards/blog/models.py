from datetime import datetime
from django.db import models



class ArticleManager(models.Manager):
    def published(self):
        return Article.objects.filter(published_at__lte=datetime.utcnow())

# Create your models here.
class Article(models.Model):

    objects = ArticleManager()

    title = models.CharField(null=False, blank=False, max_length=512)
    content = models.TextField(null=False, blank=False)
    published_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Published At')
    is_visible = models.BooleanField(default=True)

    # SEO
    keywords = models.TextField()

    class Metat:
        ordering = ['-published_data']


