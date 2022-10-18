from django.db import models
from django.conf import settings

# Create your models here.
class Link(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    # type = models.CharField(max_length=256, default='free')
    # status = models.CharField(max_length=256, default='up')
    url_code = models.CharField(max_length=256, unique=True)
    long_url = models.URLField(max_length=2048)
    view =  models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def incrementViewCount(self):
        self.viewCount += 1
        self.save()    


class Location(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    ip = models.CharField(max_length=256)
    country = models.CharField(max_length=256)
    country_code = models.CharField(max_length=256)
    