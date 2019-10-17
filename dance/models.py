from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models

# Create your models here.
from django.db.models import BooleanField


class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name


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

    name = models.CharField(max_length=100, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(Artist, on_delete=models.SET_NULL, blank=True, null=True)
    school = models.IntegerField(
        choices=SCHOOL_CHOICES,
        default=UNKNOWN,
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30, db_index=True)
    tags = models.ManyToManyField(Step, related_name='tags', blank=True)


class Video(models.Model):
    UNKNOWN = 0
    YOUTUBE = 1
    INSTAGRAM = 2
    DAILYMOTION = 3
    PLATFORM_CHOICES = [
        (UNKNOWN, 'Unknown'),
        (YOUTUBE, 'Youtube'),
        (INSTAGRAM, 'Instagram'),
        (DAILYMOTION, 'Dailymotion'),
    ]

    url = models.URLField(db_index=True)
    title = models.CharField(max_length=100, db_index=True)
    channel = models.CharField(max_length=40)
    channel_url = models.URLField()
    valid = BooleanField(default=True)
    host = models.IntegerField(
        choices=PLATFORM_CHOICES,
        default=UNKNOWN,
    )
    type = models.CharField(max_length=40)
    yid = ''

    def __init__(self, *args, **kwargs):
        super(Video, self).__init__(*args, **kwargs)

        # TODO: temporary
        if self.url and self.host == self.YOUTUBE:
            self.yid = self.url.split('v=')[1]

    def __str__(self):
        return self.title


class StepAppearance(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    time = models.IntegerField(null=True)

    class Meta:
        unique_together = [['video', 'step', 'time']]
