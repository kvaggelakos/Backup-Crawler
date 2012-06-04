### Created by Konstantinos Vaggelakos
### Used for finding interesting backups
### Use with care!

import sys
import re
import urllib2
import urlparse
from google import search


def main():
	# Init vars
	search_term = 'allinurl: /administrator/backups'

	# Check input parameters
	if (len(sys.argv) != 2):
		print 'User did not specify search term \nUsing standard search term %s' % search_term
	else:
		search_term = sys.argv[1]
		print 'Using user defined search term %s' % search_term

	# Start the search
	sites = []
	for url in search(search_term, tld='es', lang='es', stop=20):
		print url



main()
