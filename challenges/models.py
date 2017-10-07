from django.db import models


class Challenge:
    name = models.CharField(256)
    description = models.TextField()
