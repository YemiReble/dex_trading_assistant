from rest_framework import serializers
from .models import Token

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'
        
class TokenListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['id', 'name', 'symbol', 'price_usd', 'market_cap', 'volume_24h', 
                 'price_change_24h', 'recommendation', 'analysis_score']
