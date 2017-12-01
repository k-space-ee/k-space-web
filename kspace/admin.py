from django.contrib import admin
from kspace.models import *


class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'serial_nr', 'usable', 'owner', 'creator',)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'creator', None) is None:
            obj.creator = request.user
        obj.save()


class InventoryItemLocationAdmin(admin.ModelAdmin):
    list_display = ('location', 'parent',)

    class Media:
        js = ('/static/admin/js/hide_attribute.js',)

admin.site.register(Challenge)
admin.site.register(ChallengeTag)
admin.site.register(UserChallenge)
admin.site.register(Profile)
admin.site.register(InventoryItemLocation, InventoryItemLocationAdmin)
admin.site.register(InventoryItem, InventoryItemAdmin)
