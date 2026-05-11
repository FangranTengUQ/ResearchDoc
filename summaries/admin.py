from django.contrib import admin
from .models import Summary, Citation


@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'created_at', 'updated_at')
    search_fields = ('title', 'project__title')
    list_per_page = 20


@admin.register(Citation)
class CitationAdmin(admin.ModelAdmin):
    list_display = ('summary', 'resource', 'citation_number')
    list_per_page = 20
