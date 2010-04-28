import os
import django.core.handlers.wsgi

# Set the django settings and define the wsgi app
os.environ['DJANGO_SETTINGS_MODULE'] = 'dc_web.settings'
application = django.core.handlers.wsgi.WSGIHandler()

# Mount the application to the url
applications = {'/':'application', }