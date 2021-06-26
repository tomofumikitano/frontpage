import uuid

from django.utils import timezone
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Feed(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    url = models.CharField(max_length=255, null=False)
    title = models.CharField(max_length=255)
    website_url = models.CharField(max_length=255)
    date_created = models.DateTimeField('date created', default=timezone.now)
    date_updated = models.DateTimeField('date updated', default=timezone.now)
    order = models.PositiveIntegerField()
    user = models.ForeignKey(
        User, default=1, null=False, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.title} {self.order} {self.user}"


class Article(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    date_published = models.DateTimeField('date published')

    def __str__(self) -> str:
        return f"{self.date_published}: {self.title[:35]}"
