#!/usr/bin/env python
import re
from BeautifulSoup import BeautifulSoup
import mechanize
import feedparser

def get_faces(url):
  # Browser
  br = mechanize.Browser()
  br.set_handle_redirect(True)
  br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

  br = feedparser.parse(url + '?view=plays')
  statbox = BeautifulSoup(str(br)).findAll("div", {"class" :"stats-fullbox clearfix"})[-1]
  table = statbox.find("table").findAll("tr")

  currentQuarter = 0
  violationHome = 0
  violationAway = 0
  for row in table:

    # This is where we enter a new quarter
    if hasattr(row.contents[0], 'tag'):
      # Maintain quarter
      currentQuarter += 1
      if currentQuarter == 3:
        violationHome = 0
        violationAway = 0
      continue
  
    # At a faceoff
    if 'Faceoff' in str(row):
      time = row.find("td").contents[0]
   
      #face_data = str(row.findAll("td")[1].contents).split('Faceoff ')[1]
      face_data = str(row.findAll("td")[1].contents[0]).split('Faceoff ')[1]
      [players, rest] = face_data.split('won by')
      [home, away] = players.split('vs')
      rest = rest.strip()

      # REST is Winner punctuation then optionally the groundball
      winner = ''
      comma = rest.find(',')
      period = rest.find('.')
      if comma != -1:
        if period != -1:
          winner = rest[:min(comma, period)]
          rest = rest[min(comma, period) + 1:]
        else:
          winner = rest[:comma]
          rest = rest[comma + 1:]
      else:
        winner = rest[:period]
        rest = rest[period + 1:]
        
      print currentQuarter, time, home, away, winner 

    # currentQuarter, home, away, winner, time


get_faces('http://newmacsports.com/sports/mlax/2013-14/boxscores/20140315_3fn9.xml')
get_faces('http://newmacsports.com/sports/mlax/2013-14/boxscores/20140315_zg56.xml')
