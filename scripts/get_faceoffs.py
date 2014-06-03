#!/usr/bin/env python
import re
from BeautifulSoup import BeautifulSoup
import feedparser
import HTMLParser
import collections

def format_name(name):
  if len(name.split(', ')) == 2:
    name = ''.join(reversed(name.split(', ')))
    name = name.replace("  ", " ")
  if len(name.split(',')) == 2:
    name = ''.join(reversed(name.split(',')))
    name = name.replace("  ", " ")
  html_parser = HTMLParser.HTMLParser()
  name = html_parser.unescape(name)
  name = name.replace('\\', '')
  name = name.title()
  name = name.replace('Iii', 'III')
  name = name.strip()
  return name

def format_winner(winner):
  html_parser = HTMLParser.HTMLParser()
  winner = html_parser.unescape(winner)
  winner = winner.replace('\\', '')
  return winner

def decide_reason(plays_queue, quarter, time):
  # If it was the start of a quarter, make it a 0
  if quarter < 5:
    if int(time.split(':')[0]) == 15 or (int(time.split(':')[0]) == 14 and int(time.split(':')[1]) >= 58):
    # If it was this close to the start of the quarter assume it was start
      return 'QUARTER'
  else:
    if time == '4:00' or time =='04:00':
      # If it was the start of an overtime
      return 'QUARTER'

  for play in plays_queue:
    if 'goal by' in play.lower():
      goal_ind = play.lower().index('goal')
      # this play is the goal

      after_ind = play[goal_ind:]
      by = after_ind.split(' ')[2]
      if '<' in by:
        by = by.split('<')[0]
      by = by.strip()
      by = format_winner(by)
      return by

    if 'quarter' in play.lower():
      return 'QUARTER'

  return 'QUARTER'


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

    plays_queue = collections.deque(maxlen=9)

    # In case there are multiple statboxes on the page
    for box in statboxes:
      if 'Face' in str(box) and 'won by' in str(box):
        statbox = box
        break

    table = statbox.find("table").findAll("tr")
    faces = []
    currentQuarter = 0
    last_row_face = False
    current_face = None

    for row in table:
      plays_queue.appendleft(str(row))

      # This is where we enter a new quarter
      if hasattr(row.contents[0], 'tag') and row.find("th"):
        # Maintain quarter
        currentQuarter += 1

      if last_row_face and current_face:
        home = current_face[2]
        away = current_face[3]
        ind = max(str(row).find('ground'), str(row).find('Ground'), str(row).find('GB'), str(row).find('Draw'))
        gb = False
        wing_gb = False
        if ind > 0:
          if home.lower() in str(row)[ind:].lower() or away.lower() in str(row)[ind:].lower():
            gb = True
          home_flipped = ', '.join(reversed(home.split(' ')))
          away_flipped = ', '.join(reversed(away.split(' ')))
          if home_flipped.lower() in str(row)[ind:].lower() or away_flipped.lower() in str(row)[ind:].lower():
            gb = True
          if not gb:
            wing_gb = True
        is_gb = current_face[5] or gb
        is_violation = current_face[6] or 'violation' in str(row).lower()
        is_wing_gb = current_face[7] or wing_gb
        l = list(current_face)
        l[5] = is_gb
        l[6] = is_violation
        l[7] = is_wing_gb

        # This should make it easier to decide if it was the start of a quarter
        quarter_of_face = l[0]
        face_time = l[1]
        reason = decide_reason(plays_queue, quarter_of_face, face_time)
        l.append(reason)

        current_face = tuple(l)
        faces.append(current_face)
        print current_face

        current_face = None

      # last row face is whether the last row is a face
      last_row_face = False

      # At a faceoff
      if 'Faceoff' in str(row):
        last_row_face = True
        time = row.find("td").contents[0]

        face_data = str(row.findAll("td")[1].contents[0]).split('Faceoff ')[1]
        [players, rest] = face_data.split('won by')
        [away, home] = players.split('vs')
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

        winner = format_winner(winner)

        gb = False
        wing_gb = False
        ind = max(str(row).find('ground'), str(row).find('Ground'), str(row).find('GB'), str(row).find('Draw'))
        if ind > 0:
          if home.lower() in str(row)[ind:].lower() or away.lower() in str(row)[ind:].lower():
            gb = True
          home_flipped = ', '.join(reversed(home.split(' ')))
          away_flipped = ', '.join(reversed(away.split(' ')))
          if home_flipped.lower() in str(row)[ind:].lower() or away_flipped.lower() in str(row)[ind:].lower():
            gb = True
          if not gb:
            wing_gb = True

        violation = 'violation' in str(row).lower()

        current_face = (currentQuarter, time, home, away, winner, gb, violation, wing_gb)
    return faces
  except:
    return get_faces_other_type(url)


def get_faces_other_type(url):
  try:
    br = feedparser.parse(url)
    statbox = BeautifulSoup(str(br)).findAll("table", {"class" :"center_wide"})
    html_parser = HTMLParser.HTMLParser()

    plays_queue = collections.deque(maxlen=9)

    faces = []

    # Remove duplicates
    if len(statbox) % 2 == 0 and len(statbox) > 4:
      statbox = statbox[: len(statbox) / 2]
    table = [x.findAll("tr") for x in statbox]

    currentQuarter = 0
    last_row_face = False
    current_face = None

    for ind in range(len(table)):
      quarter = table[ind]
      currentQuarter = ind + 1
      for row in quarter:
        # Handle the queue of recent plays
        plays_queue.appendleft(str(row))

        # if the last fow was a faceoff
        if last_row_face and current_face:
          home = current_face[2]
          away = current_face[3]
          ind = max(str(row).find('ground'), str(row).find('Ground'), str(row).find('GB'), str(row).find('Draw'))
          gb = False
          wing_gb = False
          if ind > 0:
            if home.lower() in str(row)[ind:].lower() or away.lower() in str(row)[ind:].lower():
              gb = True
            home_flipped = ', '.join(reversed(home.split(' ')))
            away_flipped = ', '.join(reversed(away.split(' ')))
            if home_flipped.lower() in str(row)[ind:].lower() or away_flipped.lower() in str(row)[ind:].lower():
              gb = True
            if not gb:
              wing_gb = True

          is_gb = current_face[5] or gb
          is_violation = current_face[6] or 'violation' in str(row).lower()
          is_wing_gb = current_face[7] or wing_gb
          l = list(current_face)
          l[5] = is_gb
          l[6] = is_violation
          l[7] = is_wing_gb

          # This should make it easier to decide if it was the start of a quarter
          quarter_of_face = l[0]
          face_time = l[1]
          reason = decide_reason(plays_queue, quarter_of_face, face_time)
          l.append(reason)

          current_face = tuple(l)
          faces.append(current_face)
          print current_face

          current_face = None

        # last row face is whether the last row is a face
        last_row_face = False

        # At a faceoff
        if 'Faceoff' in str(row):
          last_row_face = True
          time = row.find("td").contents[0]
          time = time[1:-1]

          face_data = str(row.findAll("td")[1].contents[0]).split('Faceoff ')[1]
          [players, rest] = face_data.split('won by')
          [away , home] = players.split('vs')
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

          winner = format_winner(winner)

          gb = False
          wing_gb = False
          ind = max(str(row).find('ground'), str(row).find('Ground'), str(row).find('GB'), str(row).find('Draw'))
          if ind > 0:
            if home.lower() in str(row)[ind:].lower() or away.lower() in str(row)[ind:].lower():
              gb = True
            home_flipped = ', '.join(reversed(home.split(' ')))
            away_flipped = ', '.join(reversed(away.split(' ')))
            if home_flipped.lower() in str(row)[ind:].lower() or away_flipped.lower() in str(row)[ind:].lower():
              gb = True
            if not gb:
              wing_gb = True

          violation = 'violation' in str(row).lower()

          current_face = (currentQuarter, time, home, away, winner, gb, violation, wing_gb)
    return faces

  except :
    print 'FAIL'
    return None

if __name__ == '__main__':
  get_faces('http://middlebury.prestosports.com/sports/mlax/2013-14/boxscores/20140315_y4vr.xml?view=plays')
  #get_faces('http://www.ritathletics.com/boxscore.aspx?id=7226&path=mlax')
  #get_faces('http://www.mlc-mwlc.org/sports/mlax/2013-14/boxscores/20140423_wnd9.xml')
  #get_faces('http://www.generalssports.com/sports/mlax/2013-14/boxscores/20140329_b213.xml?view=plays')
  #get_faces('http://www.mitchellathletics.com/sports/mlax/2013-14/boxscores/20140412_v9l5.xml?view=undefined')
  #get_faces('http://www.ritathletics.com/boxscore.aspx?id=7227&path=mlax')
  #get_faces('http://www.laxmagazine.com/links/b9gzz2')
  pass

