from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from nomr import views

uuid_regex = '[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}'

urlpatterns = patterns('',
    url(r'^$', 'nomr.views.home', name='home'),
    url(r'^api/$', 'nomr.views.api_root'),
    url(r'^books/$', views.BookList.as_view(), name='book-list'),
    url(r'^books/(?P<pk>%s)/$' % uuid_regex, views.BookDetail.as_view()),
    url(r'^bookparts/$', views.BookPartList.as_view(), name='book-part-list'),
    url(r'^bookparts/(?P<pk>%s)/$' % uuid_regex, views.BookPartDetail.as_view()),
    url(r'^pages/$', views.PageList.as_view(), name='page-list'),
    url(r'^pages/(?P<pk>%s)/$' % uuid_regex, views.PageDetail.as_view()),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/', include(admin.site.urls))
)

urlpatterns += patterns('nomr.search',
    url(r'^search/$', 'search', name="search")
)
