from django.contrib import admin
from .models import ComparisonTable


@admin.register(ComparisonTable)
class ComparisonTableAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'created_at', 'updated_at')
    search_fields = ('title', 'project__title')
    list_per_page = 20
