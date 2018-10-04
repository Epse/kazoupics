from django.contrib import admin
from .models import Picture, Blocked_Poster, Sms, Blocked_Number, Ad


# Disable the "Delete" action
admin.site.disable_action('delete_selected')

def delete_hide(modeladmin, request, queryset):
    queryset.update(deleted=True)
delete_hide.short_description = "Delete from view, without actually deleting the data"

def unhide(modeladmin, request, queryset):
    queryset.update(deleted=False)
unhide.short_description = "Undelete"

@admin.register(Sms)
class SmsAdmin(admin.ModelAdmin):
    date_heirarchy = (
            'timestamp',
    )
    ordering = ['timestamp']
    list_display = (
            'sender',
            'text',
            'deleted',
            'timestamp',
    )
    readonly_fields = (
            'sender',
            'text',
            'timestamp',
    )
    actions = [delete_hide, unhide]

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    date_heirarchy = (
            'timestamp',
    )
    ordering = ['timestamp']
    list_display = (
            'poster',
            'is_ad',
            'deleted',
            'timestamp',
    )
    readonly_fields = (
            'poster',
            'is_ad',
            'timestamp',
    )
    actions = [delete_hide, unhide]

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    # Re-enable bulk deletion
    actions = ['delete_selected']

@admin.register(Blocked_Poster)
class AdAdmin(admin.ModelAdmin):
    # Re-enable bulk deletion
    actions = ['delete_selected']

@admin.register(Blocked_Number)
class AdAdmin(admin.ModelAdmin):
    # Re-enable bulk deletion
    actions = ['delete_selected']
