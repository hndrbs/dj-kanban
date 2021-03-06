"""
WSGI config for djkanban project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
import dotenv
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from django.conf import settings

dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djkanban.settings')

application = get_wsgi_application()
# application = WhiteNoise(get_wsgi_application(), root=settings.STATIC_ROOT)
