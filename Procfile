web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && python crear_admin.py && gunicorn chapikids.wsgi --bind 0.0.0.0:$PORT
