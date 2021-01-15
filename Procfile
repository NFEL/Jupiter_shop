release: python manage.py migrate
web: gunicorn jupiter_shop.wsgi:application --log-file - --log-level debug