from django.db import models
from django.contrib.auth.models import User
import uuid


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    profile_url = models.SlugField(unique=True, blank=True)  # unique link

    def save(self, *args, **kwargs):
        if not self.profile_url:
            self.profile_url = f"{self.full_name.lower().replace(' ', '-')}-{uuid.uuid4().hex[:6]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class BusinessCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # admin who added it
    full_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True, null=True)  
    company = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    profile_url = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.profile_url:
            self.profile_url = f"{self.full_name.lower().replace(' ', '-')}-{uuid.uuid4().hex[:6]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.company}"
