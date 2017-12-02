from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from location_field.models.plain import PlainLocationField
import os


def get_profile_image_path(instance, filename):
    return os.path.join('icons', str(instance.id), filename)


def get_inventory_item_path(filename):
    return os.path.join('inventory', filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    icon = models.ImageField(upload_to=get_profile_image_path, default='default_icon.png')

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
    creator = models.ForeignKey(User, blank=True, null=True, editable=False)
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(ChallengeTag, blank=True)

    def __str__(self):
        return self.name


class UserChallenge(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    challenge = models.ForeignKey(Challenge)


class InventoryItemLocation(models.Model):
    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey("self", blank=True, null=True)
    address = models.BooleanField(default=True)
    location = models.CharField(max_length=256)
    gps_location = PlainLocationField(based_fields=['location'], blank=True, null=True)

    def __str__(self):
        return self.location


class InventoryItem(models.Model):
    id = models.AutoField(primary_key=True)
    id_code = models.CharField(max_length=32, default='0123456789')
    serial_nr = models.CharField(max_length=32, default='0123456789')
    usable = models.BooleanField(default=True)
    fixable = models.BooleanField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    destroyedTime = models.DateTimeField(blank=True, null=True)
    creator = models.ForeignKey(User, related_name="%(class)s_created", blank=True, null=True, editable=False)
    location = models.ForeignKey(InventoryItemLocation, blank=True, null=True)
    owner = models.ForeignKey(User, related_name="%(class)s_item", blank=True, null=True)
    value = models.IntegerField(blank=True, null=True)
    item_name = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to=get_inventory_item_path, blank=True, null=True)

    def __str__(self):
        return self.title
