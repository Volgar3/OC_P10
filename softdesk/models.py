import uuid

from django.conf import settings
from django.db import models


class Project(models.Model):
    class ProjectType(models.TextChoices):
        BACK_END = "back-end"
        FRONT_END = "front-end"
        IOS = "iOS"
        ANDROID = "Android"

    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=10, choices=ProjectType.choices)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="authored_projects",)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Contributor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="contributions",)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="contributors",)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "project"], name="unique_contributor_per_project")]

    def __str__(self):
        return f"{self.user.username} @ {self.project.name}"


class Issue(models.Model):
    class Priority(models.TextChoices):
        LOW = "LOW"
        MEDIUM = "MEDIUM"
        HIGH = "HIGH"

    class Tag(models.TextChoices):
        BUG = "BUG"
        FEATURE = "FEATURE"
        TASK = "TASK"

    class Status(models.TextChoices):
        TO_DO = "To Do"
        IN_PROGRESS = "In Progress"
        FINISHED = "Finished"

    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=6, choices=Priority.choices)
    tag = models.CharField(max_length=7, choices=Tag.choices)
    status = models.CharField(max_length=11, choices=Status.choices, default=Status.TO_DO)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="issues",)
    author  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="authored_issues",)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_issues",)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments",)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="authored_comments",)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.uuid}"
