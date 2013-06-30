from django.conf.urls import patterns, include, url
from lecture import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', views.home, name='home'),
                       url(r'^register$',views.register, name='register'),
                       url(r'^sign_in$', views.sign_in, name='sign_in'),
                       url(r'^sign_out$', views.sign_out, name='sign_out'),
                       url(r'^post_item$', views.post_item, name='post_item'),
                       url(r'^my_items$',views.my_items, name='my_items'),
                       url(r'^admin/', include(admin.site.urls)),
                       )
