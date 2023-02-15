from django.db import models

# Create your models here.
class Log(models.Model):
    date_time = models.DateTimeField()
    writer = models.CharField(max_length=255)
    content = models.CharField(max_length=1024)
