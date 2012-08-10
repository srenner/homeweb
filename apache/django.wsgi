import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'HomeWeb.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
path = '/home/shawn/django/HomeWeb'
if path not in sys.path:
    sys.path.append(path)