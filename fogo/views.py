# Create your views here.
from fogo.models import Faceoff
from django.template import Context, loader, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect

def index(request):
    faceoffs = Faceoff.objects.all()[:10]
    return str(faceoffs)
