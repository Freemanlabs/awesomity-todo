from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()

# Create your models here.
class ToDo(models.Model):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    ACTIVE = "ACTIVE"
    DONE = "DONE"
    CLOSED = "CLOSED"
    PRIORITY_CHOICES = [(LOW, "Low"), (MEDIUM, "Medium"), (HIGH, "High")]
    STATUS_CHOICES = [(ACTIVE, "Active"), (DONE, "Done"), (CLOSED, "Closed")]

    title = models.CharField(max_length=50)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=LOW)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE)
    created_by = models.ForeignKey(UserModel, null=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
