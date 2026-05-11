from django.db import models
from projects.models import ResearchProject


def resource_upload_path(instance, filename):
    return f'resources/{instance.project.user.id}/{instance.project.id}/{filename}'


class Resource(models.Model):
    TYPE_FILE = 'file'
    TYPE_URL = 'url'
    RESOURCE_TYPES = [
        (TYPE_FILE, 'PDF File'),
        (TYPE_URL, 'URL Link'),
    ]

    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES)
    file = models.FileField(upload_to=resource_upload_path, null=True, blank=True)
    url = models.URLField(max_length=500, null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title

    @property
    def display_link(self):
        if self.resource_type == self.TYPE_FILE and self.file:
            return self.file.url
        return self.url or '#'
