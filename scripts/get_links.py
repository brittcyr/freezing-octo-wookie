#!/usr/bin/env python
from BeautifulSoup import BeautifulSoup
import feedparser
import urlparse

def get_links(conference_url = 'http://www.newmacsports.com/sports/mlax/2013-14/schedule'):
  br = feedparser.parse(conference_url)
  page = BeautifulSoup(str(br))
  links = page.findAll('a')

  parsed = urlparse.urlsplit(conference_url)
  domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed)

  link_list = []

  for link in links:
    if 'Box' in str(link) or 'boxscore' in str(link):
      url = urlparse.urljoin(domain, str(link['href']))
      link_list.append(url)
  print 'Got all links for ' + conference_url
  return link_list


def get_links_calendar(conference_url='http://www.cccathletics.com/sports/mlax/composite?date=2014-02-01'):
  prefix = conference_url[:-2]
  link_list = []

  for a in range(180):
    url = prefix + str(a)
    br = feedparser.parse(url)
    page = BeautifulSoup(str(br))
    links = page.findAll('a')

    parsed = urlparse.urlsplit(conference_url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed)


    for link in links:
      if 'Box' in str(link):
        url = urlparse.urljoin(domain, str(link['href']))
        link_list.append(url)
  print 'Got all links for ' + conference_url
  return link_list


if __name__ == "__main__":
  #print get_links()
  print get_links_calendar()
