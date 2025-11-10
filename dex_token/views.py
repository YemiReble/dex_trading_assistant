from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db import models
from rest_framework import generics, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Token
from .serializers import TokenSerializer, TokenListSerializer
from .services import update_tokens_from_api

# API Views
class TokenListAPIView(generics.ListAPIView):
    queryset = Token.objects.all()
    serializer_class = TokenListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['recommendation', 'symbol']
    search_fields = ['name', 'symbol']
    ordering_fields = ['analysis_score', 'volume_24h', 'market_cap', 'price_change_24h']
    ordering = ['-analysis_score']

class TokenDetailAPIView(generics.RetrieveAPIView):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer

class RecommendationsAPIView(generics.ListAPIView):
    serializer_class = TokenListSerializer
    
    def get_queryset(self):
        return Token.objects.filter(recommendation='BUY').order_by('-analysis_score')

@api_view(['POST'])
@csrf_exempt
def update_tokens(request):
    """Manually trigger token data update"""
    print(request)
    print("Calling Update all Token...")
    try:
        count = update_tokens_from_api()
        return Response({'success': True, 'updated_count': count})
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=500)

# Template Views
def dashboard(request):
    """Dashboard view"""
    try:
        top_tokens = Token.objects.filter(recommendation='BUY')[:10]
        total_tokens = Token.objects.count()
        buy_recommendations = Token.objects.filter(recommendation='BUY').count()
        hold_recommendations = Token.objects.filter(recommendation='HOLD').count()
        avoid_recommendations = Token.objects.filter(recommendation='AVOID').count()
        
        context = {
            'top_tokens': top_tokens,
            'total_tokens': total_tokens,
            'buy_recommendations': buy_recommendations,
            'hold_recommendations': hold_recommendations,
            'avoid_recommendations': avoid_recommendations,
        }
        return render(request, 'tokens/dashboard.html', context)
    except Exception as e:
        # Clear corrupted data and redirect
        Token.objects.all().delete()
        context = {
            'top_tokens': [],
            'total_tokens': 0,
            'buy_recommendations': 0,
            'hold_recommendations': 0,
            'avoid_recommendations': 0,
        }
        return render(request, 'tokens/dashboard.html', context)

def token_explorer(request):
    """Token explorer view"""
    try:
        tokens = Token.objects.all()[:50]
        return render(request, 'tokens/explorer.html', {'tokens': tokens})
    except Exception as e:
        return render(request, 'tokens/explorer.html', {'tokens': []})

def token_detail(request, token_id):
    """Token detail view"""
    try:
        token = get_object_or_404(Token, id=token_id)
        return render(request, 'tokens/detail.html', {'token': token})
    except Exception as e:
        # Handle decimal conversion errors
        return render(request, 'tokens/error.html', {
            'error_message': f'Error loading token data. Please try refreshing the token data.',
            'token_id': token_id
        })

def recommendations(request):
    """Recommendations view"""
    try:
        buy_tokens = Token.objects.filter(recommendation='BUY').order_by('-analysis_score')
        hold_tokens = Token.objects.filter(recommendation='HOLD').order_by('-analysis_score')[:10]
        
        context = {
            'buy_tokens': buy_tokens,
            'hold_tokens': hold_tokens,
        }
        return render(request, 'tokens/recommendations.html', context)
    except Exception as e:
        context = {
            'buy_tokens': [],
            'hold_tokens': [],
        }
        return render(request, 'tokens/recommendations.html', context)

def token_checker(request):
    """Token checker view"""
    token = None
    search_query = request.GET.get('search', '').strip()
    search_type = request.GET.get('type', 'name')
    error_message = None
    from_database = False
    
    if search_query:
        try:
            # First, search in database
            if search_type == 'address':
                token = Token.objects.filter(
                    models.Q(token_address__iexact=search_query) | 
                    models.Q(pair_address__iexact=search_query)
                ).first()
            else:
                token = Token.objects.filter(
                    models.Q(name__icontains=search_query) | 
                    models.Q(symbol__iexact=search_query)
                ).first()
            
            if token:
                from_database = True
            else:
                # If not found in database, fetch from API
                from .services import fetch_and_analyze_token
                token = fetch_and_analyze_token(search_query, search_type)
                
                if not token:
                    error_message = f"Token not found for '{search_query}'. The token may not exist or is not available on supported DEXs."
                
        except Exception as e:
            error_message = f"Error searching for token: {str(e)}"
    
    context = {
        'token': token,
        'search_query': search_query,
        'search_type': search_type,
        'error_message': error_message,
        'from_database': from_database,
    }
    return render(request, 'tokens/checker.html', context)

@api_view(['POST'])
@csrf_exempt
def update_single_token(request, token_id):
    """Update a single token from API"""
    print("Calling Update Single Token...")
    try:
        print("Token Update Request:", token_id)
        token = get_object_or_404(Token, id=token_id)
        from .services import fetch_and_analyze_token
        
        # Try to update using the token symbol first, then name
        updated_token = fetch_and_analyze_token(token.symbol, 'name')
        if not updated_token:
            updated_token = fetch_and_analyze_token(token.name, 'name')
            
        if updated_token:
            return Response({'success': True, 'message': 'Token updated successfully'})
        else:
            return Response({'success': False, 'error': 'Failed to fetch updated data'}, status=400)
            
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=500)

def about(request):
    """About view"""
    return render(request, 'tokens/about.html')
