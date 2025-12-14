from django.contrib import admin
from .models import ItemPost, ContactRequest

# Register your models here.
@admin.register(ItemPost)
class ItemPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'university', 'user', 'is_resolved', 'created_at')
    list_filter = ('university', 'is_resolved', 'created_at')
    search_fields = ('title', 'description', 'location_text')
    actions = ['mark_as_resolved']

    @admin.action(description='Mark selected items as resolved')
    def mark_as_resolved(self, request, queryset):
        queryset.update(is_resolved=True)

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'item', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('from_user__telegram_username', 'to_user__telegram_username', 'item__title')
