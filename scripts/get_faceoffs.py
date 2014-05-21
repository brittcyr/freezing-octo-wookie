#!/usr/bin/env python
import re
from BeautifulSoup import BeautifulSoup
import feedparser
import HTMLParser

def format_name(name):
  if len(name.split(', ')) == 2:
    name = ''.join(reversed(name.split(', ')))
    name = name.replace("  ", " ")
  html_parser = HTMLParser.HTMLParser()
  name = html_parser.unescape(name)
  name = name.replace('\\', '')
  name = name.title()
  return name

def get_faces(url):
  try:
    html_parser = HTMLParser.HTMLParser()
    br = feedparser.parse(url + '?view=plays')
    current_page = br['href']
    if '?view=plays' not in current_page:
      current_page += '?view=plays'
    else:
      current_page = current_page.split('?view=plays')[0] + '?view=plays'
    br = feedparser.parse(current_page)
    statboxes = BeautifulSoup(str(br)).findAll("div", {"class" :"stats-fullbox clearfix"})
    statbox = statboxes[-1]

    # In case there are multiple statboxes on the page
    for box in statboxes:
      if 'Face' in str(box) and 'won by' in str(box):
        statbox = box
        break

    table = statbox.find("table").findAll("tr")

    faces = []

    currentQuarter = 0
    violationHome = 0
    violationAway = 0
    for row in table:

      # This is where we enter a new quarter
      if hasattr(row.contents[0], 'tag') and row.find("th"):
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
        home = format_name(home)
        away = format_name(away)
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
        winner = html_parser.unescape(winner)
        
        print currentQuarter, time, home, away, winner 
        faces.append((currentQuarter, time, home, away, winner ))
    return faces
  except:
    return get_faces_other_type(url)
    # currentQuarter, home, away, winner, time


def get_faces_other_type(url):
  try:
    br = feedparser.parse(url)
    statbox = BeautifulSoup(str(br)).findAll("table", {"class" :"center_wide"})
    html_parser = HTMLParser.HTMLParser()
   
    faces = []

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
          home = format_name(home)
          away = format_name(away)
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
          winner = html_parser.unescape(winner)
        
          print currentQuarter, time, home, away, winner 
          faces.append((currentQuarter, time, home, away, winner ))
    return faces

  except :
    print 'FAIL'
    return None

if __name__ == '__main__':
  get_faces('http://www.generalssports.com/sports/mlax/2013-14/boxscores/20140329_b213.xml?view=plays')
  #get_faces('http://www.mitchellathletics.com/sports/mlax/2013-14/boxscores/20140412_v9l5.xml?view=undefined')
  #get_faces('http://www.ritathletics.com/boxscore.aspx?id=7227&path=mlax')
  #get_faces('http://www.laxmagazine.com/links/b9gzz2')
  pass
  
