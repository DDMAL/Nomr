from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from gold import views

uuid_regex = '[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}'

urlpatterns = patterns('',
    url(r'^$', 'gold.views.home', name='home'),
    url(r'^books/$', views.BookList.as_view()),
    url(r'^books/(?P<pk>%s)/$' % uuid_regex, views.BookDetail.as_view()),
    url(r'^pages/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/', include(admin.site.urls))

)
