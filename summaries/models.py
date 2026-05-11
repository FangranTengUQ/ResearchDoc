from django.db import models
from projects.models import ResearchProject
from resources.models import Resource


class Summary(models.Model):
    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE, related_name='summaries')
    title = models.CharField(max_length=200)
    content_json = models.JSONField(default=dict, blank=True)
    content_html = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name_plural = 'summaries'

    def __str__(self):
        return self.title


class Citation(models.Model):
    summary = models.ForeignKey(Summary, on_delete=models.CASCADE, related_name='citations')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='citations')
    citation_number = models.PositiveIntegerField()

    class Meta:
        ordering = ['citation_number']
        unique_together = ('summary', 'citation_number')

    def __str__(self):
        return f"[{self.citation_number}] {self.resource.title}"
