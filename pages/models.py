from django.db import models

# Create your models here.
from django.db.models import BooleanField


class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Tag(models.Model):
    name = models.CharField(max_length=30)


class Step(models.Model):
    UNKNOWN = 0
    OLD = 1
    MIDDLE = 2
    NEW = 3
    SCHOOL_CHOICES = [
        (UNKNOWN, 'Unknown'),
        (OLD, 'Old school'),
        (MIDDLE, 'Middle school'),
        (NEW, 'New school'),
    ]

    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.OneToOneField(Artist, on_delete=models.SET_NULL, null=True)
    school = models.IntegerField(
        choices=SCHOOL_CHOICES,
        default=UNKNOWN,
    )
    tags = models.ManyToManyField(Tag, related_name='steps', blank=True)


class Video(models.Model):
    UNKNOWN = 0
    YOUTUBE = 1
    INSTAGRAM = 2
    PLATFORM_CHOICES = [
        (UNKNOWN, 'Unknown'),
        (YOUTUBE, 'Youtube'),
        (INSTAGRAM, 'Instagram'),
    ]

    url = models.URLField()
    title = models.CharField(max_length=100)
    channel = models.CharField(max_length=20)
    channel_url = models.URLField()
    valid = BooleanField(default=True)
    host = models.IntegerField(
        choices=PLATFORM_CHOICES,
        default=UNKNOWN,
    )


class StepAppearance(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    time = models.IntegerField(null=True)
