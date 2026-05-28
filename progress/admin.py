from django.contrib import admin
from .models import ProgressEntry


@admin.register(ProgressEntry)
class ProgressEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'value', 'goal')
    list_filter = ('date',)
