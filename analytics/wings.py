#!/usr/bin/env python
import sys, os
sys.path.append('/afs/athena.mit.edu/user/c/y/cyrbritt/Scripts/django/fogolytics')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fogolytics.settings")
from fogo.models import Player, Game, Faceoff, Ref, Team

def determine_wing(faceoff):
  # != for booleans is the same as xor
  if faceoff.wing_gb:
    return 1 if faceoff.winner else -1
  if faceoff.wing_ct:
    return -1 if faceoff.winner else 1
  return 0

if __name__ == '__main__':
  players = Player.objects.all()
  faceoffs = Faceoff.objects.all()

  num_faces = [0] * (len(players) + 1)
  wings_score = [0] * (len(players) + 1)

  for face in faceoffs:
    wing_score = determine_wing(face)
    wings_score[face.home.id] += wing_score
    wings_score[face.away.id] -= wing_score
    num_faces[face.home.id] += 1
    num_faces[face.away.id] += 1

  num_faces[0] = 1
  for i in range(len(num_faces)):
    if num_faces[i] == 0:
      continue
    wings_score[i] = float(wings_score[i]) / num_faces[i]
    print i, wings_score[i]

