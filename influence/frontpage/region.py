from django.conf import settings
from django.template.loader import render_to_string
import os

class Region(object):
    name = 'region'
    
    def __init__(self):
        self.template = 'frontpage/%s.html' % self.name
        self.output = 'frontpage/%s_static.html' % self.name
        
    def render_to_file(self):
        template_static = os.path.join(settings.TEMPLATE_DIRS[0], self.output)
        
        out = render_to_string(self.template, self.get_context())
        f = open(template_static, 'wb')
        f.write(out.encode('utf-8'))
        f.close()
    
    def get_context(self):
        return {}