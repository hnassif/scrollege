from django.conf.urls import patterns, include, url
from lecture import views
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', views.home, name='home'),
                       url(r'^register$',views.register, name='register'),
                       url(r'^sign_in$', views.sign_in, name='sign_in'),
                       url(r'^sign_out$', views.sign_out, name='sign_out'),
                       url(r'^post_item$', views.post_item, name='post_item'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^test$', views.testDavid, name='test'),

                       # temporarily redirect the page //
                       url(r'^my_items$',views.testHenry, name='my_items'),
                       url(r'^accounts/login/$', views.sign_in),
                       url(r'^search', views.search, name='search'),
                       url(r'^messages$',views.testMessages, name='my_messages'),

                       url(r'^api/item$',views.getMessagesFromItem)
                       
                       ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

