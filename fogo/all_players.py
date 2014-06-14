# Create your views here.
from fogo.models import Player
from django.template import Context, loader, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime

def index(request):
    players = Player.objects.all()[:50]

    return render_to_response('all_players.html',
                              {
                                'players': players,
                              },
                              context_instance=RequestContext(request))
