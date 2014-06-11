from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  # Single game page
  url(r'^game/(?P<game>\d+)$', 'fogo.game.index'),

  # Single player page
  url(r'^player/(?P<player>\d+)$', 'fogo.player.index'),

  # All players aggregated stats
  url(r'^all_players$', 'fogo.all_players.index'),
)

urlpatterns += staticfiles_urlpatterns()
