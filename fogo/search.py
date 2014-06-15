# Create your views here.
from fogo.models import Player
from django.template import Context, loader, RequestContext
from django.http import HttpResponse
import json

def query(request):
    query = request.GET.get('query', '')
    if len(query) > 0:
        results = Player.objects.filter(name__istartswith=query)
        results_list = [x.name for x in results]
    else:
        results_list = []

    response = []
    for r in results_list:
      response.append({'value':r})
    response_text = json.dumps(response)

    return HttpResponse(response_text, content_type="application/json")
