#/usr/local/bin/python

import re
import urlparse
import robotparser

from download import *
from throttle import Throttle

def link_crawler(seed_url, link_regex):
	'''Crawl from the given seed URL following links matched by link_regex.
	v1.0.
	'''

	crawl_queue = [seed_url]
	# keep track which URL's have seen before
	seen = set(crawl_queue)
	rp = robotparser.RobotFileParser()

	while crawl_queue:
		url = crawl_queue.pop()

		# check url passes robots.txt restrictions
		if rp.can_fetch(user_agent, url):
			html = download4(url)
			# filter for links matching our regular expression
			for link in get_links(html):
				if re.match(link_regex, link):
					# convert relative link to absolute link
					link = urlparse.urljoin(seed_url, link)
					crawl_queue.append(link)
		else:
			print('Blocked by robots.txt: ', url)


def get_links(html):
	'''Return a list of links from html.
	'''

	# a regular expression to extract all links from the webpage
	webpage_regex = re.compile('<a[^>]_href=["\'](.*?)["\']', re.IGNORECASE)
	# list if all links from the webpage
	return webpage_regex.findall(html)


if __name__ == '__main__':
	url = 'http://example.webscraping.com'
	my_regex = '/(index|view)'
	link_crawler(url, my_regex)

		