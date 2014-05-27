#!/usr/bin/env python
from get_faceoffs import get_faces, get_faces_other_type
from get_links import get_links, get_links_calendar
from get_game_data import get_game_data
from determine_team import decide
import sys, os
sys.path.append('/afs/athena.mit.edu/user/c/y/cyrbritt/Scripts/django/fogolytics')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fogolytics.settings")
from fogo.models import Player, Game, Faceoff
import datetime

conferences = [
               'http://cacsports.com/sports/mlax/2013-14/schedule',
               'http://centennial.org/sports/mlax/2013-14/schedule',
               'http://www.landmarkconference.org/sports/mlax/2013-14/schedule',
               'http://www.neccathletics.com/sports/mlax/2013-14/schedule',
               'http://www2.northcoast.org/mlacrosse/schedule_2014',
               'http://www.saa-sports.com/sports/mlax/2013-14/schedule',
               'http://www.scacsports.com/sports/mlax/2013-14/schedule',
               'http://oac.org/sports/mlax/2013-14/schedule',
               'http://www.odaconline.com/sports/mlax/2013-14/schedule',
               'http://www.neacsports.com/sports/mlax/2013-14/schedule',
               'http://littleeast.com/sports/mlax/2013-14/schedule',
               'http://www.nescac.com/sports/mlax/2013-14/schedule',
               'http://www.newmacsports.com/sports/mlax/2013-14/schedule',
               'http://www.thegnac.com/sports/mlax/2013-14/schedule',
               'http://nacathletics.com/sports/mlax/2013-14/schedule',
              ]

conferences2 = [
                'http://www.cccathletics.com/sports/mlax/composite?date=2014-02-01',
                'http://www.mlc-mwlc.org/sports/mlax/composite?date=2014-02-01',
               ]

conferences3 = [
                'http://www.empire8.com/stats.aspx?path=mlax&year=2014',
                'http://www.csacsports.org/stats.aspx?path=mlax&year=2014&&',
                'http://libertyleagueathletics.com/stats.aspx?path=mlax&year=2014',
                'http://sunyac.com/stats.aspx?path=mlax&year=2014',
               ]

# Could not find MAC, PAC, Skyline
laxmag = 'http://www.laxmagazine.com/college_men/DIII/2013-14/schedule?date=20140101'


# Loading the game into db assuming that already checked it does not exist in db
def load_game_to_db(_date, _time, _home, _away, _site, _home_wins, _total_face, link, _away_score, _home_score):
  _date = datetime.datetime.strptime(_date, '%m/%d/%Y')
  model_game = Game(
    away=_away,
    home=_home,
    time=_time,
    date=_date,
    site=_site,
    home_wins=_home_wins,
    total_face=_total_face,
    away_score=_away_score,
    home_score=_home_score,
  )
  model_game.save()
  return model_game


if __name__ == "__main__":
#  links = get_links_calendar(laxmag)
#  links = list(set(links))
#  total = len(links)
  counter = 0
  for link in open('links.txt', 'r'):
    link = link.strip()
    print link

    # Print progress
    counter += 1
    if counter % 5 == 0:
      print 'Checked ' + str(counter)
    game_data = get_game_data(link)

    # Print the failed links to the failed_links.txt
    if game_data is None:
      f = open('failed_links.txt', 'a')
      f.write(link)
      f.write('\n')
      f.close()
      continue

    # Print the failed links to the failed_links.txt
    faces = get_faces(link)
    if not faces:
      f = open('failed_links.txt', 'a')
      f.write(link)
      f.write('\n')
      f.close()
      continue

    (date, game_time, location, away_team, home_team, home_wins, num_faces, officials_list, away_score, home_score) = game_data

    # This is for learning one team if the other is known
    team1 = faces[0][-1]
    team2 = faces[-1][-1]

    count_team1 = 0
    for face in faces:
      (currentQuarter, time, home, away, winner) = face
      if winner != team1:
        team2 = winner
      else:
        count_team1 += 1

    # determine the winner based on total number of wins
    hint = None
    if int(num_faces) != int(home_wins) * 2:
      if count_team1 == int(home_wins):
        hint = True
      else:
        hint = False

    if date[-3] == '/':
      date = date[:len(date)-2] + '2014'
    _date = datetime.datetime.strptime(date, '%m/%d/%Y')

    existing_games = Game.objects.filter(date=_date, home=home_team, away=away_team)
    if existing_games:
      game = existing_games[0]
      continue
    else:
      game = load_game_to_db(date, game_time, home_team, away_team, location, home_wins, num_faces, link, away_score, home_score)

    for face in faces:
      (currentQuarter, face_time, home, away, winner) = face
      if winner == team1:
        winner = decide(home_team, away_team, winner, other=team2, hint=hint)
      else:
        if hint is not None:
          winner = decide(home_team, away_team, winner, other=team1, hint=(not hint))
        else:
          winner = decide(home_team, away_team, winner, other=team1)

      home_player = Player.objects.filter(name=home)
      if not home_player:
        home_player =Player(name=home, team=home_team)
        home_player.save()
      else:
        home_player = home_player[0]
      away_player = Player.objects.filter(name=away)
      if not away_player:
        away_player =Player(name=away, team=away_team)
        away_player.save()
      else:
        away_player = away_player[0]

      face_time = '00:' + face_time

      f = Faceoff(
        away=away_player,
        home=home_player,
        game=game,
        winner=winner,
        time=face_time,
        quarter=currentQuarter,
      )
      f.save()

#  for conference in conferences2:
#    links = get_links_calendar(conference)
#    for link in links:
#      get_faces(link)
#  for conference in conferences3:
#    links = get_links_calendar(conference)
#    for link in links:
#      get_faces_other_type(link)
#  for conference in conferences3:
#    links = get_links(conference)
#    for link in links:
#      get_faces(link)
