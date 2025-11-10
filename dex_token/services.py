import requests
from django.conf import settings
from django.utils import timezone
from datetime import datetime
import pytz
import decimal
from decimal import Decimal
from .models import Token

class DexscreenerService:
    BASE_URL = 'https://api.dexscreener.com/latest/dex'
    # BASE_URL = 'https://api.dexscreener.com/latest/dex/search?q='
    
    @classmethod
    def fetch_tokens(cls, chain='BSC', limit=50):
        """Fetch tokens from Dexscreener API"""
        try:
            url = f"{cls.BASE_URL}/tokens"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching tokens: {e}")
            return None
    
    @classmethod
    def fetch_pairs(cls, chain='BSC'):
        """Fetch trading pairs from Dexscreener API"""
        try:
            url = f"{cls.BASE_URL}/search?q={chain}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching pairs: {e}")
            return None

class TokenAnalyzer:
    @staticmethod
    def calculate_analysis_score(token_data):
        """Calculate analysis score based on multiple metrics"""
        score = 0
        
        # Volume score (0-30 points)
        volume_24h = float(token_data.get('volume', {}).get('h24', 0))
        if volume_24h > 1_000_000:  # > 1M
            score += 30
        elif volume_24h > 100_000:  # > 100K
            score += 20
        elif volume_24h > 10_000:  # > 10K
            score += 10
        
        # Price change score (0-25 points)
        price_change_24h = float(token_data.get('priceChange', {}).get('h24', 0))
        if 0 < price_change_24h <= 20:  # Positive but not too high
            score += 25
        elif -5 <= price_change_24h < 0:  # Small negative
            score += 15
        elif price_change_24h > 20:  # Too high, risky
            score += 5
        
        # Liquidity score (0-25 points)
        liquidity = float(token_data.get('liquidity', {}).get('usd', 0))
        if liquidity > 500_000:  # > 500K
            score += 25
        elif liquidity > 100_000:  # > 100K
            score += 15
        elif liquidity > 50_000:  # > 50K
            score += 10
        
        # Market cap score (0-20 points)
        market_cap = float(token_data.get('marketCap', 0))
        if 1_000_000 <= market_cap <= 100_000_000:  # 1M-100M sweet spot
            score += 20
        elif market_cap > 100_000_000:  # > 100M
            score += 15
        elif market_cap > 100_000:  # > 100K
            score += 10
        
        return min(score, 100)  # Cap at 100
    
    @staticmethod
    def get_recommendation(score, price_change_24h):
        """Get buy/hold/avoid recommendation"""
        if score >= 70 and price_change_24h > -10:
            return 'BUY'
        elif score >= 40:
            return 'HOLD'
        else:
            return 'AVOID'
    
    @staticmethod
    def calculate_volatility_index(token_data):
        """Calculate volatility index"""
        price_changes = [
            abs(float(token_data.get('priceChange', {}).get('h1', 0))),
            abs(float(token_data.get('priceChange', {}).get('h6', 0))),
            abs(float(token_data.get('priceChange', {}).get('h24', 0))),
        ]
        return sum(price_changes) / len([x for x in price_changes if x > 0]) if any(price_changes) else 0

def safe_decimal(value, default=0):
    """Safely convert value to Decimal"""
    try:
        if value is None or value == '' or str(value).lower() in ['null', 'none', 'nan']:
            return Decimal(str(default))
        return Decimal(str(float(value)))
    except (ValueError, TypeError, decimal.InvalidOperation):
        return Decimal(str(default))


def fetch_and_analyze_token(search_query, search_type='name'):
    """Fetch and analyze a single token from API"""
    try:
        # Search in existing API data first
        url = f"{DexscreenerService.BASE_URL}/search/?q={search_query}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('pairs'):
            return None
            
        # Get the first matching pair
        pair_data = data['pairs'][0]
        base_token = pair_data.get('baseToken', {})
        
        if not base_token.get('address'):
            return None
            
        # Extract and process data
        info = pair_data.get('info', {})
        websites = info.get('websites', [])
        socials = info.get('socials', [])
        txns_24h = pair_data.get('txns', {}).get('h24', {})
        
        # Process socials
        twitter = next((s.get('handle') for s in socials if s.get('platform') == 'twitter'), None)
        telegram = next((s.get('handle') for s in socials if s.get('platform') == 'telegram'), None)
        discord = next((s.get('handle') for s in socials if s.get('platform') == 'discord'), None)
        
        # Calculate analysis metrics
        analyzer = TokenAnalyzer()
        score = analyzer.calculate_analysis_score(pair_data)
        price_change_24h = float(pair_data.get('priceChange', {}).get('h24', 0))
        recommendation = analyzer.get_recommendation(score, price_change_24h)
        volatility = analyzer.calculate_volatility_index(pair_data)
        
        # Create or update token
        token, created = Token.objects.update_or_create(
            pair_address=pair_data.get('pairAddress', ''),
            defaults={
                'name': base_token.get('name', 'Unknown'),
                'symbol': base_token.get('symbol', 'UNK'),
                'token_address': base_token.get('address'),
                'chain_id': pair_data.get('chainId'),
                'dex_id': pair_data.get('dexId'),
                'price_usd': safe_decimal(pair_data.get('priceUsd', 0)),
                'price_native': safe_decimal(pair_data.get('priceNative', 0)),
                'market_cap': int(float(pair_data.get('marketCap', 0))),
                'fdv': int(float(pair_data.get('fdv', 0))) if pair_data.get('fdv') else None,
                'volume_24h': int(float(pair_data.get('volume', {}).get('h24', 0))),
                'liquidity': int(float(pair_data.get('liquidity', {}).get('usd', 0))),
                'price_change_24h': safe_decimal(price_change_24h),
                'price_change_1h': safe_decimal(pair_data.get('priceChange', {}).get('h1', 0)),
                'price_change_7d': safe_decimal(pair_data.get('priceChange', {}).get('h7d', 0)),
                'buys_24h': txns_24h.get('buys'),
                'sells_24h': txns_24h.get('sells'),
                'image_url': info.get('imageUrl'),
                'website_url': websites[0].get('url') if websites else None,
                'twitter_handle': twitter,
                'telegram_handle': telegram,
                'discord_handle': discord,
                'pair_created_at': datetime.fromtimestamp(pair_data.get('pairCreatedAt', 0) / 1000, tz=pytz.UTC) if pair_data.get('pairCreatedAt') else None,
                'recommendation': recommendation,
                'analysis_score': safe_decimal(score),
                'volatility_index': safe_decimal(volatility),
                'stop_loss_level': safe_decimal(float(pair_data.get('priceUsd', 0)) * 0.9),
                'suggested_position_size': safe_decimal('5.0') if recommendation == 'BUY' else safe_decimal('2.0'),
            }
        )
        return token
        
    except Exception as e:
        print(f"Error fetching token: {e}")
        return None

def update_tokens_from_api():
    """Update token data from Dexscreener API"""
    service = DexscreenerService()
    analyzer = TokenAnalyzer()
    
    # Fetch data from API
    data = service.fetch_pairs('BSC')
    if not data or 'pairs' not in data:
        return False
    
    updated_count = 0
    for pair_data in data['pairs'][:50]:  # Limit to 50 tokens
        try:
            base_token = pair_data.get('baseToken', {})
            print(base_token)
            if not base_token.get('address'):
                continue
            
            # Extract additional data
            info = pair_data.get('info', {})
            websites = info.get('websites', [])
            socials = info.get('socials', [])
            txns_24h = pair_data.get('txns', {}).get('h24', {})
            
            # Process socials
            twitter = next((s.get('handle') for s in socials if s.get('platform') == 'twitter'), None)
            telegram = next((s.get('handle') for s in socials if s.get('platform') == 'telegram'), None)
            discord = next((s.get('handle') for s in socials if s.get('platform') == 'discord'), None)
            
            # Calculate analysis metrics
            score = analyzer.calculate_analysis_score(pair_data)
            price_change_24h = float(pair_data.get('priceChange', {}).get('h24', 0))
            recommendation = analyzer.get_recommendation(score, price_change_24h)
            volatility = analyzer.calculate_volatility_index(pair_data)
            
            # Update or create token
            token, created = Token.objects.update_or_create(
                pair_address=pair_data.get('pairAddress', ''),
                defaults={
                    'name': base_token.get('name', 'Unknown'),
                    'symbol': base_token.get('symbol', 'UNK'),
                    'token_address': base_token.get('address'),
                    'chain_id': pair_data.get('chainId'),
                    'dex_id': pair_data.get('dexId'),
                    'price_usd': Decimal(str(pair_data.get('priceUsd', 0))),
                    'price_native': Decimal(str(pair_data.get('priceNative', 0))),
                    'market_cap': int(float(pair_data.get('marketCap', 0))),
                    'fdv': int(float(pair_data.get('fdv', 0))) if pair_data.get('fdv') else None,
                    'volume_24h': int(float(pair_data.get('volume', {}).get('h24', 0))),
                    'liquidity': int(float(pair_data.get('liquidity', {}).get('usd', 0))),
                    'price_change_24h': Decimal(str(price_change_24h)),
                    'price_change_1h': Decimal(str(pair_data.get('priceChange', {}).get('h1', 0))),
                    'price_change_7d': Decimal(str(pair_data.get('priceChange', {}).get('h7d', 0))),
                    'buys_24h': txns_24h.get('buys'),
                    'sells_24h': txns_24h.get('sells'),
                    'image_url': info.get('imageUrl'),
                    'website_url': websites[0].get('url') if websites else None,
                    'twitter_handle': twitter,
                    'telegram_handle': telegram,
                    'discord_handle': discord,
                    'pair_created_at': datetime.fromtimestamp(pair_data.get('pairCreatedAt', 0) / 1000, tz=pytz.UTC) if pair_data.get('pairCreatedAt') else None,
                    'recommendation': recommendation,
                    'analysis_score': Decimal(str(score)),
                    'volatility_index': Decimal(str(volatility)),
                    'stop_loss_level': Decimal(str(float(pair_data.get('priceUsd', 0)) * 0.9)),
                    'suggested_position_size': Decimal('5.0') if recommendation == 'BUY' else Decimal('2.0'),
                }
            )
            updated_count += 1
            
        except Exception as e:
            print(f"Error processing token: {e}")
            continue
    
    return updated_count
