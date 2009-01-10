# python
import re
from pprint import pprint

# django
from django.contrib.flatpages.models import FlatPage

# project
from arkitektm import settings

def context(request):
    data = {'TEMPLATE_DEBUG': settings.TEMPLATE_DEBUG,
            'DEBUG': settings.DEBUG,
            'base_template': "base.html",
            'mobile_version': False,
            'mobile_user_agent': False,
            }
    
    #if settings.DEBUG:
    #    data['ADMIN_MEDIA_PREFIX'] = '/'
    #else:
    #    data['ADMIN_MEDIA_PREFIX'] = settings.ADMIN_MEDIA_PREFIX
            
    #if request.META.get('HTTP_USER_AGENT', None) and \
    #  parseUserAgent(request.META.get('HTTP_USER_AGENT')):
    #    data['mobile_user_agent'] = True
    #    if not niceboolean(request.COOKIES.get('not_mobile', False)):
    #        data['base_template'] = "mobile.html"
    #        data['mobile_version'] = True
    
    
        
    return data

