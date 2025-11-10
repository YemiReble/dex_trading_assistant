# Deployment Guide

## Quick Start (Development)

1. **Clone and Setup**
   ```bash
   cd dex-trading-assistant
   chmod +x start.sh
   ./start.sh
   ```

2. **Manual Setup**
   ```bash
   # Activate virtual environment
   source venv/bin/activate
   
   # Install dependencies
   pip install Django djangorestframework django-cors-headers requests python-decouple
   
   # Setup database
   python manage.py makemigrations
   python manage.py migrate
   
   # Load initial data
   python manage.py update_tokens
   
   # Run server
   python manage.py runserver
   ```

## Production Deployment

### Using Docker

1. **Build and Run**
   ```bash
   docker build -t dex-trading-assistant .
   docker run -p 8000:8000 dex-trading-assistant
   ```

2. **Using Docker Compose**
   ```yaml
   version: '3.8'
   services:
     web:
       build: .
       ports:
         - "8000:8000"
       environment:
         - DEBUG=False
         - SECRET_KEY=your-production-secret-key
   ```

### Manual Production Setup

1. **Server Setup**
   ```bash
   # Install system dependencies
   sudo apt update
   sudo apt install python3-pip python3-venv nginx postgresql
   
   # Create application user
   sudo useradd -m -s /bin/bash dextrading
   sudo su - dextrading
   ```

2. **Application Setup**
   ```bash
   # Clone repository
   git clone <your-repo-url> dex-trading-assistant
   cd dex-trading-assistant
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   pip install gunicorn psycopg2-binary
   ```

3. **Database Setup (PostgreSQL)**
   ```bash
   # Create database
   sudo -u postgres createdb dex_trading
   sudo -u postgres createuser dextrading
   sudo -u postgres psql -c "ALTER USER dextrading WITH PASSWORD 'your_password';"
   sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE dex_trading TO dextrading;"
   ```

4. **Environment Configuration**
   ```bash
   # Create production .env file
   cat > .env << EOF
   SECRET_KEY=your-very-secure-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-domain.com,www.your-domain.com
   DATABASE_URL=postgresql://dextrading:your_password@localhost/dex_trading
   EOF
   ```

5. **Django Setup**
   ```bash
   # Run migrations
   python manage.py migrate
   
   # Collect static files
   python manage.py collectstatic --noinput
   
   # Create superuser
   python manage.py createsuperuser
   
   # Load initial data
   python manage.py update_tokens
   ```

6. **Gunicorn Configuration**
   ```bash
   # Create gunicorn service file
   sudo tee /etc/systemd/system/dex-trading.service << EOF
   [Unit]
   Description=DEX Trading Assistant
   After=network.target
   
   [Service]
   User=dextrading
   Group=dextrading
   WorkingDirectory=/home/dextrading/dex-trading-assistant
   Environment="PATH=/home/dextrading/dex-trading-assistant/venv/bin"
   ExecStart=/home/dextrading/dex-trading-assistant/venv/bin/gunicorn --workers 3 --bind unix:/home/dextrading/dex-trading-assistant/dex_trading.sock dex_trading.wsgi:application
   
   [Install]
   WantedBy=multi-user.target
   EOF
   
   # Start and enable service
   sudo systemctl start dex-trading
   sudo systemctl enable dex-trading
   ```

7. **Nginx Configuration**
   ```bash
   # Create nginx configuration
   sudo tee /etc/nginx/sites-available/dex-trading << EOF
   server {
       listen 80;
       server_name your-domain.com www.your-domain.com;
   
       location = /favicon.ico { access_log off; log_not_found off; }
       location /static/ {
           root /home/dextrading/dex-trading-assistant;
       }
   
       location / {
           include proxy_params;
           proxy_pass http://unix:/home/dextrading/dex-trading-assistant/dex_trading.sock;
       }
   }
   EOF
   
   # Enable site
   sudo ln -s /etc/nginx/sites-available/dex-trading /etc/nginx/sites-enabled
   sudo nginx -t
   sudo systemctl restart nginx
   ```

8. **SSL Certificate (Let's Encrypt)**
   ```bash
   # Install certbot
   sudo apt install certbot python3-certbot-nginx
   
   # Get certificate
   sudo certbot --nginx -d your-domain.com -d www.your-domain.com
   ```

9. **Automated Token Updates**
   ```bash
   # Add cron job for token updates
   crontab -e
   
   # Add this line to update tokens every 5 minutes
   */5 * * * * /home/dextrading/dex-trading-assistant/venv/bin/python /home/dextrading/dex-trading-assistant/manage.py update_tokens
   ```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Required |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost,127.0.0.1` |
| `DATABASE_URL` | Database connection string | SQLite |

## Monitoring

1. **Application Logs**
   ```bash
   # View application logs
   sudo journalctl -u dex-trading -f
   
   # View nginx logs
   sudo tail -f /var/log/nginx/access.log
   sudo tail -f /var/log/nginx/error.log
   ```

2. **Health Check Endpoint**
   ```bash
   # Check if application is running
   curl http://your-domain.com/api/tokens/
   ```

## Backup

1. **Database Backup**
   ```bash
   # Create backup
   pg_dump dex_trading > backup_$(date +%Y%m%d_%H%M%S).sql
   
   # Restore backup
   psql dex_trading < backup_file.sql
   ```

2. **Application Backup**
   ```bash
   # Backup application files
   tar -czf dex_trading_backup_$(date +%Y%m%d).tar.gz /home/dextrading/dex-trading-assistant
   ```

## Troubleshooting

1. **Common Issues**
   - Check service status: `sudo systemctl status dex-trading`
   - Check nginx status: `sudo systemctl status nginx`
   - Check logs: `sudo journalctl -u dex-trading -n 50`

2. **Performance Optimization**
   - Enable database connection pooling
   - Configure Redis for caching
   - Use CDN for static files
   - Enable gzip compression in nginx
