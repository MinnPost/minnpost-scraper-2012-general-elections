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
import dumptruck
import scraperwiki
import lxml.html
import csv

urls = {
  'meta_questions': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaSupportResult/1?mediafileid=11',
  'meta_parties': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaSupportResult/1?mediafileid=5'
}

for u in urls:
  print '[%s] Scraping URL: %s...' % (u, urls[u])
  
  data = scraperwiki.scrape(urls[u])
  candidates = csv.reader(data.splitlines(), delimiter=';', quotechar='"')
  count = 0  

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
        'question_body': row[6]
      }
    elif u == 'meta_parties':
      # Party Abbreviation
      # Party Name 
      # Party ID 
      data = {
        'id': row[2],
        'party_code': row[0],
        'party_name': row[1],
        'party_id': row[2]
      }
    
    scraperwiki.sqlite.save(unique_keys = ['id'], data = data, table_name = u)
    count = count + 1

  # Output total for each category
  print '[%s] Total rows: %s' % (u, count)