# Create your views here.
from fogo.models import Player, Game, Ref, Faceoff, Team
from django.template import Context, loader, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime
from django.db.models import Sum, Count

def index(request, conference):
    teams = Team.objects.filter(conference=conference)

    players = Player.objects.filter(team__in=teams)

    for player in players:
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
            game.road = game.home != teams[0]
            game.opponent = game.home if game.road else game.away

        player.wins = sum([x.wins for x in games])
        player.num_taken = sum([x.num_taken for x in games])
        player.percent = "{0:.0f}".format(float(player.wins) / float(player.num_taken) * 100)

    return render_to_response('conference.html',
                              {
                                'conference': conference,
                                'teams': teams,
                                'players': players,
                              },
                              context_instance=RequestContext(request))
