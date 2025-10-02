from django.contrib import admin
from django.utils.html import format_html
from .models import Message, NGO, Donation


admin.site.register(Message)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_name', 'quantity', 'status', 'date_donated', 'assigned_ngo', 'show_image')
    list_filter = ('status', 'date_donated')
    search_fields = ('user__username', 'item_name')
    list_editable = ('status', 'assigned_ngo')

    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "No Image"

    show_image.short_description = 'Image'


@admin.register(NGO)
class NGOAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'email', 'contact_person', 'contact_number')  
