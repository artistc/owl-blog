from django.conf.urls.defaults import *
from views import server_error as handler500

urlpatterns = patterns( 'owl.blog.views',
    url(r'archive/?$','archive'),
    url(r'tags/?$','tags'),
    url(r'infinite/?$','infinite'),
    url(r'search/?$', 'search'),
    url(r'tag/(?P<slug>[^/]+)/?$', 'tag'),
    url(r'(?P<slug>.+)/leave-comment/?$', 'leave_comment'),
    url(r'error/(?P<code>[^/]+)/?$','error'),
    url(r'(?P<slug>[^/]+)/?$', 'article'),
    url(r'$', 'home'),
)
