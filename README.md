# DEX Trading Assistant

A Django fullstack web application that provides AI-powered cryptocurrency token analysis and trading recommendations using the Dexscreener API.

## Features

- **Real-time Token Analysis**: Fetches live data from Dexscreener API
- **AI Recommendations**: Buy/Hold/Avoid recommendations based on comprehensive scoring
- **Risk Management**: Stop-loss levels, position sizing, and volatility analysis
- **Modern UI/UX**: Responsive design with dark/light theme toggle
- **RESTful API**: Complete API endpoints for external integrations
- **Auto-refresh**: Automatic data updates every 5 minutes

## Technology Stack

- **Backend**: Django 4.2+ with Django REST Framework
- **Frontend**: HTML5, TailwindCSS, Chart.js
- **Database**: SQLite (development) / PostgreSQL (production)
- **API Integration**: Dexscreener API
- **Styling**: TailwindCSS with custom components

## Quick Start

### 1. Setup Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 4. Load Initial Data

```bash
# Update token data from Dexscreener API
python manage.py update_tokens
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## Project Structure

```
dex-trading-assistant/
├── dex_trading/           # Django project settings
├── tokens/                # Main application
│   ├── models.py         # Token data models
│   ├── views.py          # Views and API endpoints
│   ├── services.py       # Dexscreener API integration
│   ├── serializers.py    # DRF serializers
│   └── management/       # Custom management commands
├── templates/            # HTML templates
├── static/              # Static files (CSS, JS)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## API Endpoints

- `GET /api/tokens/` - List all tokens with filtering and search
- `GET /api/tokens/{id}/` - Get token details
- `GET /api/recommendations/` - Get buy recommendations
- `POST /api/update-tokens/` - Manually trigger data update

## Analysis Methodology

### Scoring System (0-100 points)

1. **Volume Analysis (30 points)**
   - >$1M volume: 30 points
   - >$100K volume: 20 points
   - >$10K volume: 10 points

2. **Price Movement (25 points)**
   - 0-20% gain: 25 points
   - Small loss (-5-0%): 15 points
   - High volatility (>20%): 5 points

3. **Liquidity (25 points)**
   - >$500K liquidity: 25 points
   - >$100K liquidity: 15 points
   - >$50K liquidity: 10 points

4. **Market Cap (20 points)**
   - $1M-$100M: 20 points
   - >$100M: 15 points
   - >$100K: 10 points

### Recommendations

- **BUY**: Score ≥70 with positive momentum
- **HOLD**: Score 40-69
- **AVOID**: Score <40

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

### Database Configuration

For production, update `settings.py` to use PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dex_trading',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Deployment

### Using Docker (Recommended)

```bash
# Build image
docker build -t dex-trading-assistant .

# Run container
docker run -p 8000:8000 dex-trading-assistant
```

### Manual Deployment

1. Set `DEBUG=False` in settings
2. Configure static files serving
3. Set up PostgreSQL database
4. Configure web server (nginx + gunicorn)
5. Set up SSL certificate

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Risk Disclaimer

⚠️ **This is not financial advice.** This application is for educational purposes only. Cryptocurrency trading involves substantial risk and may result in significant losses. Always do your own research and consider your risk tolerance before making any investment decisions.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on GitHub or contact the development team.

---

Built with ❤️ using Django and the Dexscreener API
