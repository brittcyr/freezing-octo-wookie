#!/usr/bin/env python
from BeautifulSoup import BeautifulSoup
import feedparser
import urlparse

def do_stuff():
  f = open('team_to_name.txt', 'r')
  mapping = {}
  for line in f:
    [name, team] = line.split('\t')
    mapping[name.strip()] = team.strip()

  f.close()

  for team in sorted(list(set(mapping.values()))):
    team = team.strip()
    found = False
    for a in mapping:
      if mapping[a].strip() != team:
        continue

      findings = search_for_conference(a)
      if findings:
        h = open('team_to_conference.txt', 'a')
        h.write(team + '\t' + findings)
        h.write('\n')
        h.close()
        found = True
        break

    if not found:
      g = open('no_conference.txt', 'a')
      g.write(team)
      g.write('\n')
      g.close()

def search_for_conference(team, url = 'http://www.laxmagazine.com/college_men/DIII/standings/index'):
  print team
  br = feedparser.parse(url)
  page = BeautifulSoup(str(br))

  tables = page.findAll('table')
  for table in tables:
    links = table.findAll('a')
    right_table = False
    for link in links:
      if team in str(link):
        right_table = True
        break
    if right_table:
      return table.find('h1').contents[0]

  # Check DII if not in D3
  if url == 'http://www.laxmagazine.com/college_men/DIII/standings/index':
    return search_for_conference(team, 'http://www.laxmagazine.com/college_men/DII/standings/index')

  return None


if __name__ == "__main__":
  do_stuff()
