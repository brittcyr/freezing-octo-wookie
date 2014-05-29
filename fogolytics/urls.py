from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  url(r'^$', 'fogo.views.index'),
  url(r'^game/(?P<game>\d+)$', 'fogo.game.index'),
  url(r'^player/(?P<player>\d+)$', 'fogo.player.index'),
)

urlpatterns += staticfiles_urlpatterns()
