from django.urls import path
from . import views

app_name = 'dex_token'

urlpatterns = [
    # Template views
    path('', views.dashboard, name='dashboard'),
    path('explorer/', views.token_explorer, name='explorer'),
    path('checker/', views.token_checker, name='checker'),
    path('token/<int:token_id>/', views.token_detail, name='detail'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('about/', views.about, name='about'),
    
    # API endpoints
    path('api/tokens/', views.TokenListAPIView.as_view(), name='api_tokens'),
    path('api/tokens/<int:pk>/', views.TokenDetailAPIView.as_view(), name='api_token_detail'),
    path('api/recommendations/', views.RecommendationsAPIView.as_view(), name='api_recommendations'),
    path('api/update-tokens/', views.update_tokens, name='api_update_tokens'),
    path('api/update-token/<int:token_id>/', views.update_single_token, name='api_update_single_token'),
]
