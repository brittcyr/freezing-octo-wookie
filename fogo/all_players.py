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

    player_ids = [p.id for p in players]

    f = open('fogo/RPI_data.txt')
    RPI_values = []
    for line in f:
        if len(line.split()) == 8:
            first, last, pid, percent, qualified, enough, opp_percent, opp_opp_percent = \
              line.split(' ')
        elif len(line.split()) == 9:
            name, last, _, pid, percent, qualified, enough, opp_percent, opp_opp_percent = \
              line.split(' ')
        else:
            continue
        RPI = .25 * float(percent) + .5 * float(opp_percent) + .25 * float(opp_opp_percent)

        if int(pid) in player_ids:
            RPI_values.append((RPI, int(pid)))

    RPI_values.sort()
    RPI_values.reverse()

    RPI_mapping = {}
    for i in range(len(RPI_values)):
        rank = i + 1
        RPI, pid = RPI_values[i]
        RPI_mapping[pid] = rank

    for player in players:
        player.RPI = RPI_mapping[player.id]

    f.close()

    g = open('fogo/wing_data.txt')
    wings = [0.0] * (len(Player.objects.all()) + 1)
    for line in g:
        player, wing = line.split()
        player = int(player)
	wing = float(wing)
        wings[player] = wing

    for player in players:
        player.wing = wings[player.id]

    g.close()

    home_faceoffs = Faceoff.objects.filter(quarter__gte=4).values('home') \
                                   .annotate(wins=Sum('winner')) \
                                   .annotate(num_taken=Count('winner'))
    away_faceoffs = Faceoff.objects.filter(quarter__gte=4).values('away') \
                                   .annotate(wins=Sum('winner')) \
                                   .annotate(num_taken=Count('winner'))
    face_wins = {}
    face_taken = {}

    for player in Player.objects.all():
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
        player.late_percent = float(face_wins[player.id]) / face_taken[player.id] * 100.0

    games = Game.objects.all()
    close_games = []
    for game in games:
        if abs(game.away_score - game.home_score) <= 3:
            close_games.append(game)

    home_faceoffs = Faceoff.objects.filter(quarter__gte=4).filter(game__in=close_games) \
                                   .values('home') \
                                   .annotate(wins=Sum('winner')) \
                                   .annotate(num_taken=Count('winner'))
    away_faceoffs = Faceoff.objects.filter(quarter__gte=4).filter(game__in=close_games) \
                                   .values('away') \
                                   .annotate(wins=Sum('winner')) \
                                   .annotate(num_taken=Count('winner'))
    face_wins = {}
    face_taken = {}

    for player in Player.objects.all():
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
        if face_taken[player.id] == 0:
            player.clutch = 0.00
        else:
            player.clutch = float(face_wins[player.id]) / face_taken[player.id] * 100.0
    players.sort(key=lambda k: k.percent, reverse=True)

    return render_to_response('all_players.html',
                              {
                                'players': players,
                              },
                              context_instance=RequestContext(request))
