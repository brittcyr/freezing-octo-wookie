#!/usr/bin/env python
import re
from BeautifulSoup import BeautifulSoup
import feedparser

def flip(name):
  if len(name.split(', ')) == 2:
    name = ''.join(reversed(name.split(', ')))
  return name

def get_faces(url):
  try:
    br = feedparser.parse(url + '?view=plays')
    br = feedparser.parse(br['href'] + '?view=plays')
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
   
        face_data = str(row.findAll("td")[1].contents[0]).split('Faceoff ')[1]
        [players, rest] = face_data.split('won by')
        [home, away] = players.split('vs')
        home = flip(home)
        away = flip(away)
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

        if '(' in winner:
          winner = winner.split(' (')[0]
        
        print currentQuarter, time, home, away, winner 

  except:
    get_faces_other_type(url)

    # currentQuarter, home, away, winner, time


def get_faces_other_type(url):
  try:
    br = feedparser.parse(url)
    statbox = BeautifulSoup(str(br)).findAll("table", {"class" :"center_wide"})

    # Remove duplicates
    if len(statbox) % 2 == 0 and len(statbox) > 4:
      statbox = statbox[: len(statbox) / 2]
    table = [x.findAll("tr") for x in statbox]

    currentQuarter = 0
    for ind in range(len(table)):
      quarter = table[ind]
      currentQuarter = ind + 1
      for row in quarter:
        # At a faceoff
        if 'Faceoff' in str(row):
          time = row.find("td").contents[0]
          time = time[1:-1]

          face_data = str(row.findAll("td")[1].contents[0]).split('Faceoff ')[1]
          [players, rest] = face_data.split('won by')
          [home, away] = players.split('vs')
          home = flip(home)
          away = flip(away)
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

          if '(' in winner:
            winner = winner.split(' (')[0]
        
          print currentQuarter, time, home, away, winner 

  except :
    print 'FAIL'

if __name__ == '__main__':
  get_faces('http://www.laxmagazine.com/links/b9gzz2')
  pass
  
