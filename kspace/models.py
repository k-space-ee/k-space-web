from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from location_field.models.plain import PlainLocationField
import os


def get_profile_image_path(instance, filename):
    return os.path.join('icons', str(instance.id), filename)


def get_inventory_item_path(instance, filename):
    return os.path.join('inventory', str(instance.id))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    icon = models.ImageField(upload_to=get_profile_image_path, default='default_icon.png')
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    contact_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class ChallengeTag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class InventoryItemOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, editable=False)
    name = models.CharField(max_length=64)

    def __str__(self):
        if self.user is not None:
            return self.user.username
        else:
            return self.name


class InventoryItemLocation(models.Model):
    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL)
    address = models.BooleanField(default=True)
    location = models.CharField(max_length=256)
    gps_location = PlainLocationField(based_fields=['location'], blank=True, null=True)

    def __str__(self):
        return self.location


class InventoryItem(models.Model):
    id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=256)
    serial_nr = models.CharField(max_length=32, default='', blank=True, null=True)
    hidden = models.BooleanField(default=True)
    owner = models.ForeignKey(InventoryItemOwner, related_name="%(class)s_item", blank=True, null=True,
                              on_delete=models.SET_NULL)
    value = models.IntegerField(blank=True, null=True)
    location = models.ForeignKey(InventoryItemLocation, blank=True, null=True, on_delete=models.SET_NULL)
    usable = models.BooleanField(default=True)
    fixable = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    destroyed = models.DateTimeField(blank=True, null=True)
    creator = models.ForeignKey(User, related_name="%(class)s_created", blank=True, null=True, editable=False,
                                on_delete=models.SET_NULL)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to=get_inventory_item_path, blank=True, null=True)

    def __str__(self):
        return self.item_name


class Challenge(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User, blank=True, null=True, editable=False, on_delete=models.SET_NULL)
    name = models.CharField(max_length=64)
    blurb = models.CharField(max_length=140, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    required_items = models.ManyToManyField(InventoryItem, blank=True)
    tags = models.ManyToManyField(ChallengeTag, blank=True)
    recurring = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UserChallenge(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    challenge = models.ForeignKey(Challenge, blank=True, null=True, on_delete=models.SET_NULL)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        InventoryItemOwner.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    instance.inventoryitemowner.save()
