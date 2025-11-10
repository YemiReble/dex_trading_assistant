#!/bin/bash

echo "🚀 Starting DEX Trading Assistant Setup..."

# Activate virtual environment
source venv/bin/activate

# Install dependencies (if not already installed)
echo "📦 Installing dependencies..."
# pip install Django djangorestframework django-cors-headers requests python-decouple

# Run migrations
echo "🗄️ Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
echo "👤 Creating superuser (optional)..."
echo "You can skip this by pressing Ctrl+C"
python manage.py createsuperuser || echo "Skipped superuser creation"

# Update token data
echo "📊 Fetching initial token data..."
python manage.py update_tokens

# Start development server
echo "🌐 Starting development server..."
echo "Visit http://127.0.0.1:8000 to access the application"
python manage.py runserver
