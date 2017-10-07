from django.db import models
from django.contrib.auth.models import User


class ChallengeTag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Challenge(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(ChallengeTag, blank=True)

    def __str__(self):
        return self.name


class UserChallenge(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    challenge = models.ForeignKey(Challenge)
