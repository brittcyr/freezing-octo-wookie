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
  links = get_links_calendar(laxmag)
  links = list(set(links))
  for link in links:
    print link
    game_data = get_game_data(link)
    if not game_data:
      f = open('failed_links.txt', 'a')
      f.write(link)
      f.write('\n')
      f.close()
      continue
    faces = get_faces(link)
    if not faces:
      f = open('failed_links.txt', 'a')
      f.write(link)
      f.write('\n')
      f.close()
      continue

    (date, time, location, away_team, home_team, home_wins, num_faces, officials_list) = game_data
    # TODO: Create GAME object
    # TODO: Check for duplicate

    for face in faces:
      (currentQuarter, time, home, away, winner) = face
      winner = decide(home_team, away_team, winner)

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
