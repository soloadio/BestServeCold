from django.db import models

# Create your models here.
class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=50)
    given_name = models.CharField(max_length=50)
    family_name = models.CharField(max_length=50)
    unique_id = models.CharField(max_length=500)
    email = models.CharField(max_length=50)