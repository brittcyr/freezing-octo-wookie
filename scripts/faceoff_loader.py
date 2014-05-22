#!/usr/bin/env python
from get_faceoffs import get_faces, get_faces_other_type
from get_links import get_links, get_links_calendar
from get_game_data import get_game_data
from determine_team import decide

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
    if counter < 500:
      continue
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

    (date, time, location, away_team, home_team, home_wins, num_faces, officials_list) = game_data

    #f = open('teams.txt', 'a')
    #f.write(str(home_team))
    #f.write('\n')
    #f.write(str(away_team))
    #f.write('\n')
    #f.close()


    # TODO: Check for duplicate
    # TODO: Create GAME object

    # This is for learning one team if the other is known
    team1 = faces[0][-1]
    team2 = faces[-1][-1]
    for face in faces:
      (currentQuarter, time, home, away, winner) = face
      if winner != team1:
        team2 = winner
        break
    for face in faces:
      (currentQuarter, time, home, away, winner) = face
      if winner == team1:
        winner = decide(home_team, away_team, winner, team2)
      else:
        winner = decide(home_team, away_team, winner, team1)

      # TODO: Create FACEOFF object
      

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
