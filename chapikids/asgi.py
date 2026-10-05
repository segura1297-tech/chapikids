"""
ASGI config for chapikids project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chapikids.settings')

application = get_asgi_application()
