from get_faceoffs import get_faces
from get_links import get_links

conferences = [
               'http://www.nescac.com/sports/mlax/2013-14/schedule',
               'http://www.newmacsports.com/sports/mlax/2013-14/schedule',
              ]

if __name__ == "__main__":
  for conference in conferences:
    links = get_links(conference)
    for link in links:
      get_faces(link)

