from django.conf.urls.defaults import *

from views import *
from settings import MEDIA_ROOT

urlpatterns = patterns('',

    (r'^/?$', home_page),
                       
    url(r'projects/', projects_page),
                       
    (r'^project_photos/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': MEDIA_ROOT + '/project_photos',
       'show_indexes': False}),
    
    
)
