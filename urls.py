from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from blog.feeds import BlogFeed

urlpatterns = patterns('',

    # admin & docs
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # RSS feed
    url(r'^feeds/blog/$', BlogFeed()),

    # blog app is served at the root
    url(r'^', include('owl.blog.urls')),
)
