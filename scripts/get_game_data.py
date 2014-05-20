#!/usr/bin/env python
import re
from BeautifulSoup import BeautifulSoup
import feedparser
import HTMLParser

def strip(word):
  if ':' in word:
    word = word.split(':')[1]
    word = word.strip()
  return word

# Ath. and 'Sports '
def officials_split(officials):
  if ';' in officials:
    officials = officials.split(';')
  elif ',' in officials:
    officials = officials.split(',')
  bad = ['Sports ', 'Ath.', 'Info', ' SID', 'Comm.']
  officials = [x for x in officials if not any([b in x for b in bad])]
  return [x.lstrip(' 0123456789') for x in officials]

def format_site(site):
  if '@' in site:
    site = site.split('@')[1]
  if '(' in site and ')' in site:
    site = site.split('(')[1].split(')')[0]
  site = site.replace('\\', '')
  return site.strip()

def format_team(team):
  if '#' in team:
    team = team[team.index('  ', team.index('#')):]
  if 'No. ' in team:
    team = team[team.split('No. ')[1].index(' '):]
  html_parser = HTMLParser.HTMLParser()
  team = html_parser.unescape(team)
  team = team.replace('\\', '')
  team = team.strip()
  return team

def format_time(time):
  if 'p' in time:
    time = time.split('p')[0]
  if 'a' in time:
    time = time.split('a')[0]
  if ':' not in time:
    time = time + ':00'
  return time

def get_game_data(url):
  try:
    br = feedparser.parse(url)
    statbox = BeautifulSoup(str(br)).findAll("div", {"class" :"stats-wrapper lcgame clearfix"})

    head = BeautifulSoup(str(statbox)).find("div", {"class" : "align-center"})
    location = format_site(head.contents[2])
    time = head.contents[4]
    date = time.split(' ')[0]
    time = format_time(time.split(' ')[2])
  
    header = BeautifulSoup(str(statbox)).findAll("span", {"class" : "stats-header"})
    away = header[0].contents[0]
    home = header[2].contents[0]
    away = format_team(away)
    home = format_team(home)

    face_box = [x for x in BeautifulSoup(str(statbox)).findAll("table") if "FACE" in str(x)][0]
    face_results = face_box.findAll("td")[-1].contents[0]
    home_wins = face_results.split('-')[0]
    faces = face_results.split('-')[1]
  except:
    get_game_data_other_type(url)
    return

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
  except:
    pass
  print date, time, location, away, home, home_wins, faces, officials_list
  return (date, time, location, away, home, home_wins, faces, officials_list)
  # date, time, location, away, home, home_wins, faces, officials_list

def get_game_data_other_type(url):
  stats = ''
  try:
    br = feedparser.parse(url)
    page = BeautifulSoup(str(br))

    stats= page.findAll("table", {"class" : "stats_table center_wide has_more_padding has_cell_borders"})[0]

  except:
    return None

  try:
    away = stats.findAll("tr")[1].find("td").contents[0]
    home = stats.findAll("tr")[2].find("td").contents[0]
    away = format_team(away)
    home = format_team(home)
  except:
    away = ''
    home = ''

  try:
    official_start = str(page).index("Officials")
    officials = str(page)[official_start: str(page).index('<br', official_start)]
    officials = strip(officials)
    officials_list = officials_split(officials)
  except:
    officials_list = []

  try:
    date_start = str(page).index("Date:")
    date = str(page)[date_start: str(page).index('<br', date_start)]
    date = strip(date)
  except:
    date = ''

  try:
    if "Start" in str(page):
      time_start = str(page).index("Start:")
    else:
      time_start = str(page).index("Time:")
    time = str(page)[time_start: str(page).index('<br', time_start)]
    time = format_time(strip(time))
  except:
    time = ''

  try:
    site_start = str(page).index("Site:")
    location = str(page)[site_start: str(page).index('<br', site_start)]
    location = format_site(strip(location))
  except:
    location = ''

  try:
    stats= page.findAll("table", {"class" : "center has_more_padding has_cell_borders stats_table"})
    stats = [x for x in stats if "Face" in str(x)][0]
    home_wins = stats.find("tbody").find("tr").findAll("td")[-1].contents[0]
    away_wins = stats.find("tbody").findAll("tr")[-1].findAll("td")[-1].contents[0]
    faces = int(home_wins) + int(away_wins)
  except:
    home_wins = 0
    away_wins = 0
    faces = 0

  print date, time, location, away, home, home_wins, faces, officials_list
  return (date, time, location, away, home, home_wins, faces, officials_list)

  # date, time, location, away, home, home_wins, faces, officials_list

if __name__ == "__main__":
  get_game_data('http://www.laxmagazine.com/links/xwxm4g')
  get_game_data('http://www.laxmagazine.com/links/k5pmhe')
  get_game_data('http://newmacsports.com/sports/mlax/2013-14/boxscores/20140315_3fn9.xml')
  get_game_data('http://newmacsports.com/sports/mlax/2013-14/boxscores/20140315_zg56.xml')
  get_game_data('http://www.cmsvathletics.com/boxscore.aspx?path=mlax&id=2735')
  get_game_data('http://www.centenarycyclones.com/boxscore.aspx?path=mlax&id=3022')
