from django.conf.urls.defaults import *


import django.views.static
from django.contrib import admin
admin.autodiscover()

# project
from settings import MEDIA_ROOT


urlpatterns = patterns('',
    # Example:
    (r'', include('www.urls')),

    # Uncomment the next line to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line for to enable the admin:
    (r'^admin/(.*)', admin.site.root),

    # CSS, Javascript and IMages
    (r'^images/(?P<path>.*)$', django.views.static.serve,
     {'document_root': MEDIA_ROOT + '/images',
       'show_indexes': True}),                       
    (r'^css/(?P<path>.*)$', django.views.static.serve,
      {'document_root': MEDIA_ROOT + '/css',
       'show_indexes': True}),
    (r'^javascript/(?P<path>.*)$', django.views.static.serve,
      {'document_root': MEDIA_ROOT + '/javascript',
       'show_indexes': True}),
)
