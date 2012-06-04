### Created by Konstantinos Vaggelakos
### Used for finding interesting backups
### Use with care!

import sys
import re
import urllib2
import urlparse
from google import search


# Global vars
search_query = 'allinurl: %(search_term)s filetype:%(filetype)s'


# This is the main entry point for the application and will start searching immidiately after validating the input parameters
def main():
	# Check input parameters
	if (len(sys.argv) != 4):
		start_search('/administrator/backups', 'sql', 20)
	else:
		start_search(sys.argv[1], sys.argv[2], sys.argv[3])


# start_search will init the search for the given search term
# @search_term The search term to search for when looking for 
# @filetype The filetype to look for
# @limit the upper limit of hosts to look into
def start_search(search_term, filetype, limit):
	print_settings(search_term, filetype, limit)
	# Start the search
	for url in search(search_query % vars(), stop=limit):
		print 'Digging into: %s' % url
		handle_url(url)


# This method will check for more backups in the same directory if directory listing is available
# @url The url should be a url to an existing sql backup file
def handle_url(url, filetype):
	# Get the relative path and get the html to search for links to other backup files
	links = download_html(url[0:url.rfind('/')])
	if (links == None):
		print 'There was a problem looking into that path, downloading file found by google'
		if (download_file(url, 'a') == None): # Change name
			print 'Couldn\'t even download the file pointed out by google'
		else:
			print 'Sucessfully downloaded: %s' % url
	else:
		# Go through all links and see if they are of sql file type
		for link in links:
			if (link.find('.%s' % filetype) == None):
				print link + '%s was not of type: %s' % (link, filetype)
			else:
				if (download_file(link, 'a') == None): #TODO: Change name
					print 'There was a problem in downloading the file: %s' % link
				else:
					print 'Downloaded file: %s\' successfully!' % link


def download_html(url):
	try:
		return urllib2.urlopen(url).read()
	except urllib2.URLError as e:
		print 'There was an error trying to download the file: %s' % url
		return None


def download_file(url, filename):
	try:
		url_handle = urllib2.urlopen(url)
		localFile = open('downloaded/%s' % filename, 'w')
		localFile.write(url_handle.read())
		localFile.close()
	except:
		print 'There was an error trying to download the file: %s' % url
		return None


def extract_urls(text):
	url_re = re.compile(r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))')
	for match in url_re.finditer(your_text):
		yield match.group(0)



# Prints the settings specified by the user
def print_settings(search_term, filetype, limit):
	print 'Search term: \'%s\'' % search_term
	print 'File type: %s' % filetype
	print 'Limit results: %i' % limit
	print 'Resulting query: \'%s\'' % search_query % vars()

main()
