from django.db import models
from django.utils import timezone

class Submission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    background_info = models.TextField()
    involved_students = models.TextField()
    submit_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
