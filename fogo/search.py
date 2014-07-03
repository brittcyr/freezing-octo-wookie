# Create your views here.
from fogo.models import Player
from django.template import Context, loader, RequestContext
from django.http import HttpResponse
import json

def query(request):
    query = request.GET.get('query', '')
    if len(query) > 0:
        results = Player.objects.filter(name__icontains=query)

    response = []
    for r in results:
      link = '/fogolytics/player/' + str(r.id)
      response.append({'value':r.name, 'link':link})
    response_text = json.dumps(response)

    return HttpResponse(response_text, content_type="application/json")
