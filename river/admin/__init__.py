from django.contrib import admin
from river.admin.proceeding_meta import ProceedingMetaAdmin
from river.models import State
from river.models import Transition


@admin.register(State)
class StateAdmin(admin.ModelAdmin):

    list_display = ('label',
                    'slug',
                    'description')

    ordering = ('label',)


@admin.register(Transition)
class TransitionAdmin(admin.ModelAdmin):

    list_display = ('__str__',
                    'source_state',
                    'destination_state',
                    'direction')

    ordering = ('source_state',)
