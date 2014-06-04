#!/usr/bin/env python
from BeautifulSoup import BeautifulSoup
import feedparser
import HTMLParser
import sys, os
sys.path.append('/afs/athena.mit.edu/user/c/y/cyrbritt/Scripts/django/fogolytics')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fogolytics.settings")
from fogo.models import Team

def get_logos(url):
  br = feedparser.parse(url)
  soup = BeautifulSoup(str(br)).findAll('td')

  teams = Team.objects.all()
  for team in teams:
    name = team.name

    for td in soup:
      if name in str(td):
        # This is where we are in the correct td element
        team.logo = td.find('img')['src']
        team.save()

def do_logo():
  get_logos('http://www.laxmagazine.com/college_men/DII/teams/index')
  get_logos('http://www.laxmagazine.com/college_men/DIII/teams/index')

if __name__ == "__main__":
  get_logos('http://www.laxmagazine.com/college_men/DII/teams/index')
  get_logos('http://www.laxmagazine.com/college_men/DIII/teams/index')
