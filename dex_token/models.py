from django.db import models
from django.utils import timezone

class Token(models.Model):
    RECOMMENDATION_CHOICES = [
        ('BUY', 'Buy'),
        ('HOLD', 'Hold'),
        ('AVOID', 'Avoid'),
    ]
    
    # Basic token info
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20)
    pair_address = models.CharField(max_length=100, unique=True)
    token_address = models.CharField(max_length=100, null=True, blank=True)
    chain_id = models.CharField(max_length=50, null=True, blank=True)
    dex_id = models.CharField(max_length=50, null=True, blank=True)
    
    # Price and market data
    price_usd = models.DecimalField(max_digits=20, decimal_places=10)
    price_native = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    market_cap = models.BigIntegerField()
    fdv = models.BigIntegerField(null=True, blank=True)
    volume_24h = models.BigIntegerField()
    liquidity = models.BigIntegerField()
    price_change_24h = models.DecimalField(max_digits=10, decimal_places=4)
    price_change_1h = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    price_change_7d = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    
    # Transaction data
    buys_24h = models.IntegerField(null=True, blank=True)
    sells_24h = models.IntegerField(null=True, blank=True)
    
    # Token info
    image_url = models.URLField(null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
    twitter_handle = models.CharField(max_length=100, null=True, blank=True)
    telegram_handle = models.CharField(max_length=100, null=True, blank=True)
    discord_handle = models.CharField(max_length=100, null=True, blank=True)
    
    # Timestamps
    pair_created_at = models.DateTimeField(null=True, blank=True)
    
    # Analysis fields
    recommendation = models.CharField(max_length=5, choices=RECOMMENDATION_CHOICES, default='HOLD')
    analysis_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    volatility_index = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    stop_loss_level = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    suggested_position_size = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-analysis_score', '-volume_24h']
    
    def __str__(self):
        return f"{self.name} ({self.symbol})"
