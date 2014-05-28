# Create your views here.
from fogo.models import Player, Game, Ref, Faceoff
from django.template import Context, loader, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.db.models import Sum
import datetime

def index(request, game):
    game = Game.objects.filter(id=game)[0]
    faceoffs = Faceoff.objects.filter(game=game)

    return render_to_response('game.html',
                              {
                                'game': game,
                                'faceoffs': faceoffs,
                              },
                              context_instance=RequestContext(request))
