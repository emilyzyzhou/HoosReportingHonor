from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from storages.backends.s3boto3 import S3Boto3Storage
from django.utils import timezone
from django.core.files.storage import default_storage
import uuid


# to import into any module: from shared.models import Report, File

class Report(models.Model):
    class Status(models.TextChoices):
        NEW = 'NEW'
        PENDING = 'PENDING'
        APPROVED = 'APPROVED'
        REJECTED = 'REJECTED'

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    incident_date = models.DateField(default=timezone.now)  # include default for existing models in db
    incident_category = models.CharField(max_length=255, default='Unknown')
    incident_location = models.CharField(max_length=255, default='Unknown')
    students_involved = models.TextField(default='Unknown')
    report_text = models.TextField(default="")  # THIS IS THE FIELD FOR EDITING NOTES
    report_summary = models.TextField(default='summary to be provided')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    report_hash = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        ordering = ['-submission_date']
        indexes = [
            models.Index(fields=['submission_date', 'status', 'incident_date', 'incident_location']),
        ]

    def __str__(self):
        user_display = self.user.username if self.user else 'Anonymous'
        return f'{self.id}: {user_display} - {self.report_summary}'

    def get_students_involved_list(self):
        """Return a list of student IDs."""
        return self.students_involved.split(', ')

    def delete(self, *args, **kwargs):
        # handle s3 file deletion
        files = self.file_set.all()
        for file in files:
            try:
                default_storage.delete(file.file.name)
            except Exception as e:
                print(f"Error deleting file {file.file.name}: {e}")
            file.delete()
        # delete the report object from db
        super(Report, self).delete(*args, **kwargs)


class File(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    file = models.FileField(storage=S3Boto3Storage(), upload_to='uploads/')

    class Meta:
        indexes = [
            models.Index(fields=['report', 'file']),
        ]

    def get_file_url(self):
        return self.file.url

    def __str__(self):
        return f'{self.report.id}: {self.file}'


# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}: {self.is_admin}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
