#!/usr/bin/env python
from BeautifulSoup import BeautifulSoup
import mechanize
import feedparser
import urlparse

def get_links(conference_url = 'http://www.newmacsports.com/sports/mlax/2013-14/schedule'):
  # Browser
  br = mechanize.Browser()
  br.set_handle_redirect(True)
  br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

  br = feedparser.parse(conference_url)
  page = BeautifulSoup(str(br))
  links = page.findAll('a')
  
  parsed = urlparse.urlsplit(conference_url)
  domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed)

  link_list = []
  
  for link in links:
    if 'Box Score' in str(link) or 'Stats' in str(link):
      url = urlparse.urljoin(domain, str(link['href']))
      link_list.append(url)
  print 'Got all links'
  return link_list

if __name__ == "__main__":
  print get_links()
