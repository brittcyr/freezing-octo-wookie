from get_faceoffs import get_faces
from get_links import get_links, get_links_calendar

conferences = [
               'http://littleeast.com/sports/mlax/2013-14/schedule',
               'http://www.nescac.com/sports/mlax/2013-14/schedule',
               'http://www.newmacsports.com/sports/mlax/2013-14/schedule',
               'http://www.thegnac.com/sports/mlax/2013-14/schedule',
              ]

conferences2 = [
                'http://www.cccathletics.com/sports/mlax/composite?date=2014-02-01',
               ]

if __name__ == "__main__":
  for conference in conferences:
    links = get_links(conference)
    for link in links:
      get_faces(link)
  for conference in conferences2:
    links = get_links_calendar(conference)
    for link in links:
      get_faces(link)

