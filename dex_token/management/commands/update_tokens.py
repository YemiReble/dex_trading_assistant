from django.core.management.base import BaseCommand
from dex_token.services import update_tokens_from_api

class Command(BaseCommand):
    help = 'Update token data from Dexscreener API'

    def handle(self, *args, **options):
        self.stdout.write('Starting token data update...')
        
        try:
            count = update_tokens_from_api()
            if count:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully updated {count} tokens')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('No tokens were updated')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error updating tokens: {e}')
            )
