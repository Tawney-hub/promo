from django.contrib import admin
from .models import CampaignLocation, PromoCode, Lead, ScanLog

@admin.register(CampaignLocation)
class CampaignLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'reward_type', 'is_active')
    list_filter = ('reward_type', 'is_active')

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'location', 'unlocked_code', 'created_at')
    list_filter = ('location', 'created_at')
    search_fields = ('full_name', 'phone', 'email')

@admin.register(ScanLog)
class ScanLogAdmin(admin.ModelAdmin):
    list_display = ('location', 'ip_address', 'scanned_at')
    list_filter = ('location', 'scanned_at')
