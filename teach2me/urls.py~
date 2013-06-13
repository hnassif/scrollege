from django.conf.urls import patterns, include, url
from lecture import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', views.home, name='home'),
                       url(r'^sign_in$', views.sign_in, name='sign_in'),
                       url(r'^sign_out$', views.sign_out, name='sign_out'),
		       url(r'^display$', views.showItems),
                       #url(r'^post_data', views.post_data),
                       #url(r'^mystats', views.session_stats),
                       #url(r'^prof', views.prof_graph),
                       #url(r'^post_qn', views.rec_qn),
                       #url(r'^stream$', views.stream),
                       #url(r'^stream_qn$', views.stream_qn),
                       #url(r'^graph_data$', views.graph_data),
                       # url(r'^teach2me/', include('teach2me.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/',
                       # include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),

                       )
