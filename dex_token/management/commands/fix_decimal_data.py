from django.core.management.base import BaseCommand
from django.db import connection
from decimal import Decimal, InvalidOperation

class Command(BaseCommand):
    help = 'Fix invalid decimal values in Token model'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Get all decimal columns that might have invalid values
            decimal_fields = [
                'price_usd', 'price_native', 'price_change_24h', 
                'price_change_1h', 'price_change_7d', 'analysis_score',
                'volatility_index', 'stop_loss_level', 'suggested_position_size'
            ]
            
            for field in decimal_fields:
                try:
                    # Update NULL or invalid decimal values
                    if field in ['price_usd', 'price_change_24h', 'analysis_score', 'volatility_index']:
                        # Required fields - set to 0
                        cursor.execute(f"UPDATE dex_token_token SET {field} = '0' WHERE {field} IS NULL OR {field} = '' OR {field} = 'NaN' OR {field} = 'Infinity' OR {field} = '-Infinity'")
                    else:
                        # Optional fields - set to NULL
                        cursor.execute(f"UPDATE dex_token_token SET {field} = NULL WHERE {field} = '' OR {field} = 'NaN' OR {field} = 'Infinity' OR {field} = '-Infinity'")
                    
                    self.stdout.write(f"Fixed {field}: {cursor.rowcount} rows updated")
                except Exception as e:
                    self.stdout.write(f"Error fixing {field}: {e}")
        
        self.stdout.write(self.style.SUCCESS('Successfully fixed decimal data'))
