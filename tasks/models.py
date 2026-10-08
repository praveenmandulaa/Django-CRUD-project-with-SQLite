from django.conf import settings
from django.db import models
class Task(models.Model):
    class Status(models.TextChoices):
        TODO = 'todo', 'To do'
        PROGRESS = 'progress', 'In progress'
        DONE = 'done', 'Done'
    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, max_length=3000)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.TODO)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at', '-id']
        indexes = [models.Index(fields=['owner', 'status'])]
    def __str__(self):
        return self.title
