from django.core.management.base import BaseCommand
from dex_token.models import Token

class Command(BaseCommand):
    help = 'Clean up corrupted token data'

    def handle(self, *args, **options):
        self.stdout.write('Cleaning up corrupted token data...')
        
        try:
            # Delete all tokens to clear corrupted data
            count = Token.objects.count()
            Token.objects.all().delete()
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted {count} corrupted tokens')
            )
            self.stdout.write('You can now run "python manage.py update_tokens" to fetch fresh data')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error cleaning up tokens: {e}')
            )
