from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os


def get_image_path(instance, filename):
    return os.path.join('icons', str(instance.id), filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    icon = models.ImageField(upload_to=get_image_path, default='default_icon.png')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class ChallengeTag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Challenge(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User)
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(ChallengeTag, blank=True)

    def __str__(self):
        return self.name


class UserChallenge(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    challenge = models.ForeignKey(Challenge)
