# Create your views here.
from fogo.models import Player, Game, Ref, Faceoff
from django.template import Context, loader, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime
from django.db.models import Sum, Count

def index(request, player):
    player = Player.objects.filter(id=player)[0]
    team = player.team
    home_faceoffs = Faceoff.objects.filter(home=player) \
                                   .values('game_id') \
                                   .annotate(wins=Sum('winner')) \
                                   .annotate(num_taken=Count('winner'))
    away_faceoffs = Faceoff.objects.filter(away=player) \
                                   .values('game_id') \
                                   .annotate(wins=Sum('winner')) \
                                   .annotate(num_taken=Count('winner'))
    # Have to flip this because wins are 0 on the road
    for face in away_faceoffs:
        face['wins'] = face['num_taken'] - face['wins']

    faceoffs = [x for x in home_faceoffs] + [y for y in away_faceoffs]
    game_ids = [x['game_id'] for x in faceoffs]

    # All games with one of these faceoffs
    games = Game.objects.filter(id__in=game_ids).order_by('date')

    for game in games:
      game.wins = int(sum([x['wins'] for x in faceoffs if x['game_id'] == game.id]))
      game.num_taken = sum([x['num_taken'] for x in faceoffs if x['game_id'] == game.id])
      game.percent = "{0:.0f}".format(float(game.wins) / float(game.num_taken) * 100)
      game.opponent = game.home if game.home != team else game.away

    wins = sum([x.wins for x in games])
    num_taken = sum([x.num_taken for x in games])
    percent = "{0:.0f}".format(float(wins) / float(num_taken) * 100)

    return render_to_response('player.html',
                              {
                                'player': player,
                                'games': games,
                                'wins': wins,
                                'num_taken': num_taken,
                                'percent': percent,
                                'team': team,
                              },
                              context_instance=RequestContext(request))
