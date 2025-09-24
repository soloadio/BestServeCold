from django.db import models
from User.models import User


class Draft(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=50)
    subject = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=50)
    content = models.JSONField()
    # website = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

class Batch(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drafts = models.ManyToManyField(Draft, related_name="batches")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Batch {self.id} for {self.user.full_name}"