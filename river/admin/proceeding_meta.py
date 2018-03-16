from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
from django.utils.html import format_html_join
from django.utils.translation import ugettext_lazy as _
from river.models import ProceedingMeta
from river.models.fields.state import StateField
from river.services.object import ObjectService


def get_content_types():
    content_type_pks = []
    for ct in ContentType.objects.all():
        model = ct.model_class()
        if model is not None:
            for f in model._meta.fields:
                if type(f) is StateField:
                    content_type_pks.append(ct.pk)
    return content_type_pks


class ProceedingMetaForm(forms.ModelForm):
    content_type = forms.ModelChoiceField(queryset=ContentType.objects.none())

    class Meta:
        model = ProceedingMeta
        fields = ('content_type', 'transition', 'permissions', 'groups', 'order', 'action_text')

    def __init__(self, *args, **kwargs):
        self.declared_fields['content_type'].queryset = ContentType.objects.filter(
            pk__in=get_content_types())

        super(ProceedingMetaForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        content_type = self.cleaned_data['content_type']
        field = ObjectService.get_field(content_type.model_class())
        instance = super(ProceedingMetaForm, self).save(commit=False)
        instance.field = field.name
        return super(ProceedingMetaForm, self).save(*args, **kwargs)


class ProceedingMetaAdmin(admin.ModelAdmin):
    form = ProceedingMetaForm

    def permissions_list(self, obj):
        if obj.permissions.count() > 0:
            return format_html(
                '<ul>{}</ul>',
                format_html_join(
                    '\n', '<li>{}</li>',
                    obj.permissions.values_list('name')))

    permissions_list.short_description = _('Permissions')
    permissions_list.admin_order_field = 'permissions'

    def groups_list(self, obj):
        if obj.groups.count() > 0:
            return format_html(
                '<ul>{}</ul>',
                format_html_join(
                    '\n', '<li>{}</li>',
                    obj.groups.values_list('name')))

    groups_list.short_description = _('Groups')
    groups_list.admin_order_field = 'groups'

    list_display = ('content_type',
                    'transition',
                    'permissions_list',
                    'groups_list',
                    'order',
                    'action_text')

    ordering = ('content_type', 'transition', 'order')


admin.site.register(ProceedingMeta, ProceedingMetaAdmin)
