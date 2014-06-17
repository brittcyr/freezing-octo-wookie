# Create your views here.
from django.template import Context, loader, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):

    return render_to_response('index.html',
                              {
                                  # Fill in the index data if needed
                              },
                              context_instance=RequestContext(request))
