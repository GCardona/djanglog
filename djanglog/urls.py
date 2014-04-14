from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djanglog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'article.views.article_all'),
    url(r'^article/all/$', 'article.views.article_all'),
    url(r'^article/(?P<article_id>\d+)/$', 'article.views.article_detail'),
    url(r'^article/new/$', 'article.views.article_new'),
    url(r'^need_login/$', 'djanglog.views.need_login'),
)

