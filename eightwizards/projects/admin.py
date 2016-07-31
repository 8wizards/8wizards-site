import logging
from django.contrib import admin
from django.forms import ModelForm
from .models import Project, MediaResource, Skill, Category

logger = logging.getLogger(__name__)


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    form = SkillForm
    list_display = ('name', 'description')


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    list_display = ('name', 'slug', 'description')


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'


class MediaInline(admin.StackedInline):
    model = MediaResource
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm
    inlines = [MediaInline]
    list_display = ('name', 'status', 'category')
    list_filter = ('status', 'category')
