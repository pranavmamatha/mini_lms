#!/usr/bin/env bash
# Mini LMS - Quick Setup Script
set -e

echo "🎓 Setting up Mini LMS..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️  Running migrations..."
python manage.py makemigrations accounts
python manage.py makemigrations courses
python manage.py migrate

# Create superuser (optional)
echo ""
echo "Would you like to create a superuser (admin)? [y/N]"
read -r CREATE_SUPER
if [[ "$CREATE_SUPER" =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# Collect static files (optional for dev)
# python manage.py collectstatic --noinput

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Start the server with:"
echo "   python manage.py runserver"
echo ""
echo "Then open: http://127.0.0.1:8000"
echo "  Admin:   http://127.0.0.1:8000/admin/"
