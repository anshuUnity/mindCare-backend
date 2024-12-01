from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

class VideoCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'video_category'
        verbose_name = 'Video Category'
        verbose_name_plural = 'Video Categories'

    def __str__(self):
        return self.name

    def clean(self):
        # Validation to ensure name is not empty or too short
        if len(self.name.strip()) < 3:
            raise ValueError("Category name must be at least 3 characters long.")


class Video(models.Model):
    category = models.ForeignKey(VideoCategory, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    url = models.URLField()
    thumbnail = models.URLField()
    duration = models.IntegerField(validators=[MinValueValidator(1)], help_text="Duration in seconds")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'video'
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    def __str__(self):
        return self.title

    def clean(self):
        # Validate URL and duration
        if not self.url.startswith('http'):
            raise ValueError("URL must be a valid HTTP or HTTPS link.")
        if self.duration <= 0:
            raise ValueError("Duration must be a positive integer.")

