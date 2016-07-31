import logging
from django.contrib import admin
from django.forms import ModelForm
from .models import Role, PromoUrl, Member, Certification

logger = logging.getLogger(__name__)


class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = '__all__'


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    form = RoleForm
    list_display = ('name', 'description')


class PromoInline(admin.StackedInline):
    model = PromoUrl
    extra = 1


class CertificationInline(admin.StackedInline):
    model = Certification
    extra = 1


class MemberForm(ModelForm):
    class Meta:
        model = Role
        fields = '__all__'


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    form = RoleForm
    date_hierarchy = 'birthday'
    inlines = [PromoInline, CertificationInline]
    list_display = ('first_name', 'last_name', 'role', 'nick_name', 'is_available')


