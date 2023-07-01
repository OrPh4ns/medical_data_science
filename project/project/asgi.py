"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Set the default Django settings module in the environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
# Create the ASGI application
application = get_asgi_application()
