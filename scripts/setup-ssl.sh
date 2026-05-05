#!/bin/bash

# SSL Setup Script for MLOps Project
# This script sets up Nginx with SSL certificates using Certbot

set -e

DOMAIN="mlops.tejasvaij.com"
EMAIL="tejas.vaij@gmail.com"  # Update this with your email

echo "Setting up SSL for $DOMAIN..."

# Create necessary directories
mkdir -p certbot/conf certbot/www

# Stop existing services if running
echo "Stopping existing services..."
docker-compose -f docker-compose.yml down || true
docker-compose -f docker-compose.ssl.yml down || true

# Generate initial SSL certificate
echo "Generating SSL certificate..."
docker-compose -f docker-compose.ssl.yml --profile init up certbot-init

# Wait for certificate generation
echo "Waiting for certificate generation..."
sleep 10

# Check if certificate was generated
if [ -f "certbot/conf/live/$DOMAIN/fullchain.pem" ]; then
    echo "✅ SSL certificate generated successfully!"
else
    echo "❌ SSL certificate generation failed!"
    exit 1
fi

# Start all services with SSL
echo "Starting services with SSL..."
docker-compose -f docker-compose.ssl.yml up -d

echo "✅ SSL setup complete!"
echo "🌐 Your application is now available at: https://$DOMAIN"
echo "📊 Monitoring endpoints:"
echo "   - Prometheus: https://$DOMAIN/prometheus"
echo "   - Grafana: https://$DOMAIN/grafana"

# Show status
docker-compose -f docker-compose.ssl.yml ps
