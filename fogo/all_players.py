# Create your views here.
from fogo.models import Player, Faceoff, Team, Game
from django.template import Context, loader, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db.models import Sum, Count

def index(request):
    players = Player.objects.all()

    home_faceoffs = Faceoff.objects.values('home') \
                                   .annotate(wins=Sum('winner')) \
                                   .annotate(num_taken=Count('winner'))
    away_faceoffs = Faceoff.objects.values('away') \
                                   .annotate(wins=Sum('winner')) \
                                   .annotate(num_taken=Count('winner'))
    face_wins = {}
    face_taken = {}

    for player in players:
        face_wins[player.id] = 0
        face_taken[player.id] = 0

    for face in away_faceoffs:
        face['wins'] = face['num_taken'] - face['wins']
        face_wins[face['away']] = face['wins']
        face_taken[face['away']] = face['num_taken']

    for face in home_faceoffs:
        face_wins[face['home']] += face['wins']
        face_taken[face['home']] += face['num_taken']

    for player in players:
        player.wins = face_wins[player.id]
        player.num_taken = face_taken[player.id]
        player.percent = float(player.wins) / player.num_taken * 100.0

    teams = Team.objects.all()
    home_faceoffs = Game.objects.values('home') \
                                 .annotate(wins=Sum('home_wins')) \
                                 .annotate(total=Sum('total_face'))
    away_faceoffs = Game.objects.values('away') \
                                 .annotate(wins=Sum('home_wins')) \
                                 .annotate(total=Sum('total_face'))

    team_faces = [0]*(len(teams)*2)
    for face in away_faceoffs:
        team_faces[face['away']] = face['total']
    for face in home_faceoffs:
        team_faces[face['home']] += face['total']

    players = list(players)
    players = [p for p in players if (p.num_taken > .4 * team_faces[p.team.id] and p.num_taken > 50)]

    return render_to_response('all_players.html',
                              {
                                'players': players,
                              },
                              context_instance=RequestContext(request))
