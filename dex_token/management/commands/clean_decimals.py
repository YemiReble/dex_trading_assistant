from django.core.management.base import BaseCommand
from dex_token.models import Token
from decimal import Decimal, InvalidOperation

class Command(BaseCommand):
    help = 'Clean invalid decimal values in Token model'

    def handle(self, *args, **options):
        tokens = Token.objects.all()
        fixed_count = 0
        
        for token in tokens:
            try:
                # Try to access all decimal fields to trigger the error
                _ = token.price_usd
                _ = token.price_change_24h
                _ = token.analysis_score
            except Exception as e:
                self.stdout.write(f"Found problematic token: {token.id}")
                # Delete the problematic token
                token.delete()
                fixed_count += 1
        
        self.stdout.write(f"Removed {fixed_count} problematic tokens")
        
        # Also clean any remaining tokens with extreme values
        Token.objects.filter(price_usd__gt=Decimal('1000000000')).delete()
        Token.objects.filter(price_usd__lt=Decimal('0')).delete()
        
        self.stdout.write(self.style.SUCCESS('Database cleaned successfully'))
