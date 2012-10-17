#!/usr/bin/env python
"""
Scraper for the 2012 general election in Minnesota.  Main
results page can be found here:

http://electionresults.sos.state.mn.us/enr/ENR/Home/1
http://electionresults.sos.state.mn.us/ENR/Select/Download/1

Describing file columns:

http://electionresults.sos.state.mn.us/ENR/Select/DownloadFileFormats/1



This file gets meta data.
"""
import re
import scraperwiki
import csv
import datetime
import calendar
import logging
import os

# Set up logger.  Check file first
log_file = os.path.join(os.path.dirname(__file__), './logs/scraping.log')
if not os.path.exists(os.path.dirname(log_file)):
  os.makedirs(os.path.dirname(log_file))
logger = logging.getLogger('scraper_meta')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)
logger.info('[scraper] Scraping Meta data tables.')

urls = {
  'meta_questions': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaSupportResult/1?mediafileid=11',
  'meta_parties': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaSupportResult/1?mediafileid=5'
}

for u in urls:
  data = scraperwiki.scrape(urls[u])
  candidates = csv.reader(data.splitlines(), delimiter=';', quotechar='"')
  count = 0
  # Make a UTC timestamp
  timestamp = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

  for row in candidates:
    if u == 'meta_questions':
      # County ID 
      # Office Code
      # MCD code, if applicable (using FIPS statewide unique codes, not county MCDs)
      # School District Numbe, if applicable
      # Ballot Question Number
      # Question Title
      # Question Body
      data = {
        'id': row[0] + '-' + row[1],
        'county_id': row[0],
        'office_code': row[1],
        'mcd_fips_code': row[2],
        'school_district': row[3],
        'question_number': row[4],
        'question_title': row[5],
        'question_body': row[6],
        'updated': int(timestamp)
      }
    elif u == 'meta_parties':
      # Party Abbreviation
      # Party Name 
      # Party ID 
      data = {
        'id': row[2],
        'party_code': row[0],
        'party_name': row[1],
        'party_id': row[2],
        'updated': int(timestamp)
      }
    
    scraperwiki.sqlite.save(unique_keys = ['id'], data = data, table_name = u)
    count = count + 1

  # Output total for each category
  logger.info('[%s] Total rows: %s' % (u, count))