from django.contrib import admin
from .models import Token

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol', 'price_usd', 'market_cap', 'volume_24h', 
                   'price_change_24h', 'recommendation', 'analysis_score']
    list_filter = ['recommendation', 'created_at']
    search_fields = ['name', 'symbol', 'pair_address']
    ordering = ['-analysis_score']
    readonly_fields = ['created_at', 'updated_at']
