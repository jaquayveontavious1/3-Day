from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Sprint(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sprints')
    title = models.CharField(max_length=255)

    start_datetime = models.DateTimeField(default=timezone.now)
    end_datetime = models.DateTimeField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    visibility = models.CharField(max_length=20,default='public',blank=True)
    def save(self, *args, **kwargs):
        # Automatically set end time to 72 hours after start
        if not self.end_datetime:
            self.end_datetime = self.start_datetime + timedelta(hours=72)
        super().save(*args, **kwargs)

    def progress_percentage(self):
        total = self.goals.count()
        if total == 0:
            return 0
        completed = self.goals.filter(is_completed=True).count()
        return int((completed / total) * 100)

    def check_and_update_status(self):
        if self.progress_percentage() == 100:
            self.status = 'COMPLETED'
            self.save()
        elif timezone.now() > self.end_datetime and self.status == 'ACTIVE':
            self.status = 'FAILED'
            self.save()
    @property
    def remaining_seconds(self):
        remaining = self.end_datetime - timezone.now()
        return max(int(remaining.total_seconds()), 0)

    def __str__(self):
        return f"{self.title} - {self.user.email}"


class Goal(models.Model):
    sprint = models.ForeignKey(
        Sprint,
        on_delete=models.CASCADE,
        related_name='goals'
    )

    text = models.CharField(max_length=255)

    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def mark_complete(self):
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save()

        # After completing a goal, check sprint status
        self.sprint.check_and_update_status()

    def __str__(self):
        status = "Done" if self.is_completed else "Pending"
        return f"{self.text} ({status})"
# Create your models here.
class SprintUserStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, related_name="user_statuses")
    status = models.CharField(
        max_length=20,
        choices=[
            ("Not Started", "Not Started"),
            ("In Progress", "In Progress"),
            ("Paused", "Paused"),
            ("Completed", "Completed")
        ],
        default="Not Started"
    )
    progress = models.PositiveIntegerField(default=0) 

# models.py
class SprintHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sprint = models.ForeignKey('Sprint', on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sprint.title} - {self.user.username}"
