import django
import os

django.setup()

from populate import gearstore

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'settings.settings')

gearstore.populate()
