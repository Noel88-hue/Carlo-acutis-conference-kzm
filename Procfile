release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn carlo_acutis.wsgi --log-file -
