Project Description:
Build a Django Fullstack Web Application that provides token recommendations and holding strategies using Dexscreener’s API. The web app should fetch real-time token data, analyze valid tokens, and recommend which ones are good to buy and hold. The application must have an intuitive UI, smooth navigation, and a responsive, modern design for both desktop and mobile users.

⚙️ Core Requirements
Backend (Django)

Framework: Django (latest stable version)

Core Functionality:

Connect to the Dexscreener API to fetch live data for valid tokens.

Store token information such as:

Token name, symbol, price, market cap, 24h volume, liquidity, price change, and pair address.

Analyze tokens using metrics like:

Price movement trend

Volume growth rate

Liquidity strength

Market cap ranking

Generate “Buy” or “Hold” recommendations based on the analysis.

Implement a risk management module that calculates:

Stop-loss levels

Suggested position size

Volatility index

API Layer:

Create Django REST Framework endpoints:

/api/tokens/ → list all analyzed tokens

/api/tokens/<id>/ → view token details

/api/recommendations/ → show recommended tokens

Include pagination, filtering (by name, market cap, volume), and search.

Database: PostgreSQL (or SQLite for local development)

Caching: Use Redis or Django cache framework for faster API responses.

Background Tasks: Celery + Redis for scheduled token data updates.

Security & Best Practices:

Environment variable management via .env

CSRF & CORS enabled for frontend integration

Input validation for user queries

Use DRF serializers and proper error handling

Frontend (React or Django Templates)

UI/UX:

Clean, minimal dashboard-style interface.

Dark and light themes toggle.

Mobile responsive (TailwindCSS or Bootstrap).

Core Pages:

Home/Dashboard: Overview of top-performing tokens and their summary cards.

Token Explorer: Detailed table of all tracked tokens with sorting and filtering.

Token Detail Page: Shows live stats, price charts (using Chart.js or Recharts), and AI-driven recommendation (“Buy”, “Hold”, or “Avoid”).

Recommendations Page: Displays current buy/hold tokens with performance metrics.

About/Info Page: Explains how the analysis and recommendations work.

Navigation: Sticky header with routes:

Home | Explorer | Recommendations | About

Interactivity:

Dynamic charts

Real-time price refresh

Search bar for tokens

Loading states and error messages for API data fetch

🧩 Recommendation Engine Logic

Algorithm:

Compute an internal score for each token using weighted metrics: