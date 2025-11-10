from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from .models import Token

class TokenModelTest(TestCase):
    def setUp(self):
        self.token = Token.objects.create(
            name="Test Token",
            symbol="TEST",
            pair_address="0x123456789",
            price_usd=Decimal('1.50'),
            market_cap=1000000,
            volume_24h=500000,
            liquidity=250000,
            price_change_24h=Decimal('5.25'),
            recommendation='BUY',
            analysis_score=Decimal('75.50')
        )

    def test_token_creation(self):
        self.assertEqual(self.token.name, "Test Token")
        self.assertEqual(self.token.symbol, "TEST")
        self.assertEqual(self.token.recommendation, 'BUY')

    def test_token_str(self):
        self.assertEqual(str(self.token), "Test Token (TEST)")

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.token = Token.objects.create(
            name="Test Token",
            symbol="TEST",
            pair_address="0x123456789",
            price_usd=Decimal('1.50'),
            market_cap=1000000,
            volume_24h=500000,
            liquidity=250000,
            price_change_24h=Decimal('5.25'),
            recommendation='BUY',
            analysis_score=Decimal('75.50')
        )

    def test_dashboard_view(self):
        response = self.client.get(reverse('tokens:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "DEX Trading Dashboard")

    def test_explorer_view(self):
        response = self.client.get(reverse('tokens:explorer'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Token Explorer")

    def test_token_detail_view(self):
        response = self.client.get(reverse('tokens:detail', args=[self.token.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Token")

    def test_api_tokens_list(self):
        response = self.client.get(reverse('tokens:api_tokens'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Token")
