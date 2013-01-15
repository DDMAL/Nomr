from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

uuid_regex = '[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}'

urlpatterns = patterns('',
    url(r'^$', 'gold.views.home', name='home'),
    url(r'^books/$', 'gold.views.book_list'),
    url(r'^books/(?P<uuid>%s)/$' % uuid_regex, 'gold.views.book_detail'),
    url(r'^pages/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/', include(admin.site.urls))

)
