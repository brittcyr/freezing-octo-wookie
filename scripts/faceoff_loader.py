from get_faceoffs import get_faces
from get_links import get_links

if __name__ == "__main__":
  links = get_links()
  for link in links:
    get_faces(link)

