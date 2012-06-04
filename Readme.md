# Backup-Crawler
This little python script will search google for a string to look for old backups of databases and complete sites.

The idea of doing this script started when I realized my backup plugin for wordpress just stored my backups in '/administrator/backups'. I soon started googling and found out that others had their backups stored there as well, however (probably) not knowing about it. The plugin used is called Xcloner.


## How to use

### Needed packages 
* BeautifulSoup (easy_install BeautifulSoup)
* httplib2 (easy_install httplib2)

### Running
To run this with no arguments (using defaults) just run:
python crawler.py 

To run this and specify search term and limit run:
python crawler.py [search_term] [limit]