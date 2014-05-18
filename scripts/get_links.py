#!/usr/bin/env python
from BeautifulSoup import BeautifulSoup
import mechanize
import feedparser
import urlparse

def get_links(conference_url = 'http://www.newmacsports.com/sports/mlax/2013-14/schedule'):
  links = []
  # Browser
  br = mechanize.Browser()
  br.set_handle_redirect(True)
  br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

  br = feedparser.parse(conference_url)
  schedule = BeautifulSoup(str(br)).find('table', {"class" : "schedule"})
  rows = schedule.findAll('tr')
  
  parsed = urlparse.urlsplit(conference_url)
  domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed)

  for row in rows:
    for link in row.findAll('a'):
      if 'Box Score' in str(link):
        url = urlparse.urljoin(domain, str(link['href']))
        links.append(url)
        break
  print 'Got all links'
  return links

if __name__ == "__main__":
  print get_links()
