from django.contrib import admin
from .models import ResearchProject


@admin.register(ResearchProject)
class ResearchProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description', 'user__username')
    list_per_page = 20
