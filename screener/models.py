from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from taggit.managers import TaggableManager

# Create your models here.
class Employer(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "Employer"
        verbose_name_plural = "Employers"

class Job(models.Model):
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    seniority = models.CharField(max_length=20)
    tags = TaggableManager()

    def __str__(self):
        return self.title
    
class ScreeningQuestion(models.Model):
    job = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    is_custom = models.BooleanField()
    is_approved = models.BooleanField()
    rating = models.IntegerField(null=True)

class TemplateQuestion(models.Model):
    tag = models.CharField(max_length=200)
    template_text = models.TextField()
    