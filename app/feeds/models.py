from django.utils import timezone
from django.db import models


class Feed(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    home_url = models.CharField(max_length=255)
    date_created = models.DateTimeField('date created', default=timezone.now)

    def __str__(self) -> str:
        return self.title


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    date_published = models.DateTimeField('date published')

    def __str__(self) -> str:
        return self.title
