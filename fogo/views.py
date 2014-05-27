# Create your views here.
from fogo.models import Player, Game, Ref, Faceoff
from django.template import Context, loader, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.db.models import Sum


def index(request):
    faceoffs = Faceoff.objects.all()[:100]

    return render_to_response('index.html',
                              {
                                'faceoffs': faceoffs,
                              },
                              context_instance=RequestContext(request))
