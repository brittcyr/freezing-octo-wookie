#!/usr/bin/env python
import sys, os
sys.path.append('/afs/athena.mit.edu/user/c/y/cyrbritt/Scripts/django/fogolytics')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fogolytics.settings")
from fogo.models import Player, Game, Faceoff, Ref, Team

# Whether a player has more than the threshold of faces
def has_enough_faces(player, number):
  away_face = Faceoff.objects.filter(away=player)
  home_face = Faceoff.objects.filter(home=player)
  return len(away_face) + len(home_face) >= number

# Player's FO percent on the year
def get_percent(player):
  away_face = Faceoff.objects.filter(away=player)
  home_face = Faceoff.objects.filter(home=player)

  wins = sum([1 - face.winner for face in away_face]) + sum([face.winner for face in home_face])
  total_taken = len(away_face) + len(home_face)

  return float(wins) / float(total_taken) * 100.0

# Player has taken enough of the team faceoffs
def is_qualified(player, qualifying_threshold = .4 ):
  team = player.team
  players = Player.objects.filter(team=team)

  num_faces = len(Faceoff.objects.filter(home__in=players)) + len(Faceoff.objects.filter(away__in=players))
  player_faces = len(Faceoff.objects.filter(home=player)) + len(Faceoff.objects.filter(away=player))

  return player_faces >= num_faces * qualifying_threshold

def get_opponent_percent(player, winning_percent):
  away_face = Faceoff.objects.filter(away=player)
  home_face = Faceoff.objects.filter(home=player)
  total_faces = len(away_face) + len(home_face)

  away_ids = [f.home.id for f in away_face]
  home_ids = [f.away.id for f in home_face]

  away_percents = sum([winning_percent[x] for x in away_ids])
  home_percents = sum([winning_percent[x] for x in home_ids])

  return (away_percents + home_percents) / total_faces

if __name__ == '__main__':
  players = Player.objects.all()
  winning_percent = [0] * (len(players) + 1)
  opponent_winning_percent = [0] * (len(players) + 1)
  opponent_opponent_winning_percent = [0] * (len(players) + 1)
  # qualified and has_enough are here to keep the D2 guys out
  qualified = set([])
  has_enough = set([])
  for player in players:
    winning_percent[player.id] = get_percent(player)

    # Determine whether a player has enough faces to count in RPI
    if has_enough_faces(player, 20):
      has_enough.add(player)

    # Decide whether a player qualifies by having enough of the team's faceoffs
    if is_qualified(player):
      qualified.add(player)

  for player in players:
    # Decide which players should count in the OWP (opponent winning percent)
    opponent_winning_percent[player.id] = get_opponent_percent(player, winning_percent)

  for player in players:
    # Decide the OOWP (opponents opponents winning percent)
    # which conveniently can be determined in O(n) using the same function with the
    # output of previously computed as the winning_percents
    opponent_opponent_winning_percent[player.id] = get_opponent_percent(player, opponent_winning_percent)

  for player in players:
    print player.name, player.id, winning_percent[player.id], (player in qualified), \
          (player in has_enough), \
          opponent_winning_percent[player.id], opponent_opponent_winning_percent[player.id]
