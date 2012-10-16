"""
Scraper for the 2012 general election in Minnesota.  Main
results page can be found here:

http://electionresults.sos.state.mn.us/enr/ENR/Home/1
http://electionresults.sos.state.mn.us/ENR/Select/Download/1

Describing file columns:

http://electionresults.sos.state.mn.us/ENR/Select/DownloadFileFormats/1



This file gets districts data.
"""
import re
import dumptruck
import scraperwiki
import lxml.html
import csv

urls = {
  'district_counties': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaSupportResult/1?mediafileid=6',
  'district_precincts': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaSupportResult/1?mediafileid=4',
  'district_municipal': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaSupportResult/1?mediafileid=8',
  'district_school': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaSupportResult/1?mediafileid=18',
}

for u in urls:
  print '[%s] Scraping URL: %s...' % (u, urls[u])
  
  data = scraperwiki.scrape(urls[u])
  candidates = csv.reader(data.splitlines(), delimiter=';', quotechar='|')
  count = 0  

  for row in candidates:
    if u == 'district_counties':
      # County ID
      # County Name
      # Number of precincts
      data = {
        'id': row[0],
        'county_id': row[0],
        'county_name': row[1],
        'precincts': row[2]
      }
    elif u == 'district_precincts':
      # County ID
      # Precinct ID 
      # Precinct Name
      # Congressional District 
      # Legislative District 
      # County Commissioner District 
      # Judicial District 
      # Soil and Water District 
      # MCD code (uses FIPS statewide unique codes, not county MCDs)
      # (IS NOT THERE) School District Number (school district reporting precincts only)
      data = {
        'id': row[1],
        'county_id': row[0],
        'precinct_id': row[1],
        'precinct_name': row[2],
        'congressional_district': row[3],
        'leg_district': row[4],
        'county_commissioner_district': row[5],
        'judicial_district': row[6],
        'soil_water_district': row[7],
        'mcd_fips_code': row[8]
        #'school_district': row[9]
      }
    elif u == 'district_municipal':
      # County ID
      # County Name
      # MCD code (using FIPS statewide unique codes, not county MCDs)
      # Municipality Name
      data = {
        'id': row[2],
        'county_id': row[0],
        'county_name': row[1],
        'mcd_fips_code': row[2],
        'mcd_name': row[3]
      }
    elif u == 'district_school':
      # School District Number
      # School District Name
      # County ID (Home county for school district)
      # County Name (Home county for school district)
      data = {
        'id': row[0] + '-' + row[2],
        'district_number': row[0],
        'district_name': row[1],
        'county_id': row[2],
        'county_name': row[3]
      }
    
    scraperwiki.sqlite.save(unique_keys = ['id'], data = data, table_name = u)
    count = count + 1

  # Output total for each category
  print '[%s] Total rows: %s' % (u, count)