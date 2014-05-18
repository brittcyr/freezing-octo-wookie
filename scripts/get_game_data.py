#!/usr/bin/env python
import re
from BeautifulSoup import BeautifulSoup
import mechanize
import feedparser

def get_game_data(url):
  # Browser
  br = mechanize.Browser()
  br.set_handle_redirect(True)
  br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

  br = feedparser.parse(url)
  statbox = BeautifulSoup(str(br)).findAll("div", {"class" :"stats-wrapper lcgame clearfix"})

  head = BeautifulSoup(str(statbox)).find("div", {"class" : "align-center"})
  location = head.contents[2]
  time = head.contents[4]
  date = time.split(' ')[0]
  time = time.split(' ')[2]

  
  header = BeautifulSoup(str(statbox)).findAll("span", {"class" : "stats-header"})
  away = header[0].contents[0]
  home = header[2].contents[0]


  face_box = [x for x in BeautifulSoup(str(statbox)).findAll("table") if "FACE" in str(x)][0]
  face_results = face_box.findAll("td")[-1].contents[0]
  home_wins = face_results.split('-')[0]
  faces = face_results.split('-')[1]

  officials_list = []
  try:
    officials = [x for x in BeautifulSoup(str(statbox)).findAll("td") if "Officials" in str(x)][0]
    officials = officials.findAll("span")
    for a in xrange(len(officials) - 1, 0, -1):
      official = officials[a]
      if "Officials" in str(official):
        break
      else:
        officials_list.append(str(official.contents[0]))
  except IndexError:
    pass

  # date, time, location, away, home, home_wins, faces, officials_list
get_game_data('http://newmacsports.com/sports/mlax/2013-14/boxscores/20140315_3fn9.xml')
get_game_data('http://newmacsports.com/sports/mlax/2013-14/boxscores/20140315_zg56.xml')
