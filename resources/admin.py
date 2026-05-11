from django.contrib import admin
from .models import Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'resource_type', 'created_at')
    list_filter = ('resource_type',)
    search_fields = ('title', 'description', 'project__title')
    list_per_page = 20
