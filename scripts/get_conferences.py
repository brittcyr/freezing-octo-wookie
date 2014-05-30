#!/usr/bin/env python
from BeautifulSoup import BeautifulSoup
import feedparser
import urlparse

def do_stuff():
  f = open('team_to_name.txt', 'r')
  mapping = {}
  for line in f:
    [name, team] = line.split('\t')
    mapping[name] = team

  f.close()

  for team in sorted(mapping.values()):
    found = False
    for a in mapping:
      if mapping[a] != team:
        continue

      findings = search_for_conference(a)
      if findings:
        found = True
        break

    if not found:
      g = open('no_conference.txt', 'a')
      g.write(team)
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
