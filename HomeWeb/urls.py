from django.conf.urls.defaults import patterns, include, url
from billminder.models import Bill
from django.views.generic import ListView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.decorators import login_required
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'HomeWeb.views.home', name='home'),
    # url(r'^HomeWeb/', include('HomeWeb.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    
    url(r'^admin/', include(admin.site.urls)),
    
    #url(r'^BillMinder/$', login_required(
    #    ListView.as_view(
    #                     queryset=Bill.objects.all(),
    #                     context_object_name='bills',
    #                     template_name='BillMinder/index.html'
    #                     )
    #    )),

    url(r'^BillMinder/$', 'HomeWeb.billminder.views.index'),

    url(r'^BillMinder/(?P<bill_id>\d+)/$', 'HomeWeb.billminder.views.detail'),

    url(r'^BillMinder/(?P<bill_id>\d+)/pay/$', 'HomeWeb.billminder.views.make_payment'),
    
    url(r'^BillMinder/(?P<bill_id>\d+)/history/$', 'HomeWeb.billminder.views.get_payments'),
    
    url(r'^BillMinder/alerts/$', 'HomeWeb.billminder.views.get_alerts', {'only_new': False, 'process': False}),
    
    url(r'^BillMinder/alerts/new/$', 'HomeWeb.billminder.views.get_alerts', {'only_new': True, 'process': False}),
    
    url(r'^BillMinder/alerts/process/', 'HomeWeb.billminder.views.get_alerts', {'only_new': True, 'process': True}),
    #get_payments(request, bill_id, how_many)
    
    url(r'^BillMinder/logout/$', 'HomeWeb.billminder.views.logout_view')
)
