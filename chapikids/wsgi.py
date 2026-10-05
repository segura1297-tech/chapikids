"""
WSGI config for chapikids project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chapikids.settings')

application = get_wsgi_application()
