# -*- coding:utf-8 -*-
from django.conf.urls.defaults import *
from events.models import Event, EventCategory

day_dict = {
    'date_field': 'startdate',
    'queryset': Event.objects.all(),
    'allow_future': True,
    'month_format': '%m',
}
month_dict = dict( day_dict, allow_empty=True )
urlpatterns = patterns('django.views.generic.date_based',
    # <year>/<month>/<day>/<event_id>/
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<object_id>\d+)/$',
        'object_detail', day_dict),
)


urlpatterns = urlpatterns + patterns('events.views',
    (r'^preview/$', 'preview',),
    #
    # <year>/<month>/tags/<tags>/
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/tags/(?P<tags>[a-zA-Z_\-]+)/$',
        'custom_archive_month', month_dict),
    # <year>/<month>/<category>/
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<category>[a-zA-Z_\-]+)/$', 
        'custom_archive_month', month_dict),
    # <year>/<month>/<category>/<tags>/
    #
    # <year>/<month>/
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'custom_archive_month', month_dict),
    #
    (r'^$', 'redirect_month', ),
    (r'^tags/', 'redirect_month', ),
    (r'^\d+/x', 'redirect_month', ),
)
