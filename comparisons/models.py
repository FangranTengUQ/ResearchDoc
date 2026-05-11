from django.db import models
from projects.models import ResearchProject


class ComparisonTable(models.Model):
    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE, related_name='comparisons')
    title = models.CharField(max_length=200)
    table_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title
