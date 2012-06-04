### Created by Konstantinos Vaggelakos
### Used for finding interesting backups
### Use with care!

import sys
import re
import urllib2
import urlparse
from google import search

search_query = 'allinurl: %(search_term)s filetype:%(filetype)s'

"""
This is the main entry point for the application and will start searching immidiately after validating the input parameters
"""
def main():
	# Check input parameters
	if (len(sys.argv) != 4):
		start_search('/administrator/backups', 'sql', 20)
	else:
		start_search(sys.argv[1], sys.argv[2], sys.argv[3])

"""
start_search will init the search for the given search term
@search_term The search term to search for when looking for 
@filetype The filetype to look for
@limit the upper limit of hosts to look into
"""
def start_search(search_term, filetype, limit):
	print_settings(search_term, filetype, limit)
	# Start the search
	for url in search(search_query % vars(), stop=limit):
		print handle_url(url)

"""
This method will check for more backups in the same directory if directory listing is available
@url The url should be a url to an existing sql backup file
"""
def handle_url(url):
	# Get the relative path
	rel_path = url[0:url.rfind('/')]
	return rel_path

"""
Prints the settings specified by the user
"""
def print_settings(search_term, filetype, limit):
	print 'Search term: \'%s\'' % search_term
	print 'File type: %s' % filetype
	print 'Limit results: %i' % limit
	print 'Resulting query: \'%s\'' % search_query % vars()

main()
