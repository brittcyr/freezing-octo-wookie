#!/usr/bin/env python
import re
from BeautifulSoup import BeautifulSoup
import feedparser

def get_game_data(url):
  try:
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
    officials = [x for x in BeautifulSoup(str(statbox)).findAll("td") if "Officials" in str(x)][0]
    officials = officials.findAll("span")
    for a in xrange(len(officials) - 1, 0, -1):
      official = officials[a]
      if "Officials" in str(official):
        break
      else:
        officials_list.append(str(official.contents[0]))
  # date, time, location, away, home, home_wins, faces, officials_list
  except:
    return get_game_data_other_type(url)

def get_game_data_other_type(url):
  br = feedparser.parse(url)
  page = BeautifulSoup(str(br))

  stats= page.findAll("table", {"class" : "stats_table center_wide has_more_padding has_cell_borders"})[0]
  away = stats.findAll("tr")[1].find("td").contents[0]
  home = stats.findAll("tr")[2].find("td").contents[0]

  official_start = str(page).index("Official")
  officials = str(page)[official_start: str(page).index('<br', official_start)]

  date_start = str(page).index("Date")
  date = str(page)[date_start: str(page).index('<br', date_start)]

  time_start = str(page).index("Time")
  time = str(page)[time_start: str(page).index('<br', time_start)]

  site_start = str(page).index("Site")
  location = str(page)[site_start: str(page).index('<br', site_start)]

  stats= page.findAll("table", {"class" : "center has_more_padding has_cell_borders stats_table"})
  stats = [x for x in stats if "Face" in str(x)][0]
  home_wins = stats.find("tbody").find("tr").findAll("td")[-1].contents[0]
  away_wins = stats.find("tbody").findAll("tr")[-1].findAll("td")[-1].contents[0]
  faces = int(home_wins) + int(away_wins)

  # date, time, location, away, home, home_wins, faces, officials_list


#get_game_data('http://newmacsports.com/sports/mlax/2013-14/boxscores/20140315_3fn9.xml')
#get_game_data('http://newmacsports.com/sports/mlax/2013-14/boxscores/20140315_zg56.xml')
#get_game_data('http://www.cmsvathletics.com/boxscore.aspx?path=mlax&id=2735')
