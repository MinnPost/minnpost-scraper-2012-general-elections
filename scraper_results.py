#!/usr/bin/env python
"""
Scraper for the 2012 general election in Minnesota.  Main
results page can be found here:

http://electionresults.sos.state.mn.us/enr/ENR/Home/1
http://electionresults.sos.state.mn.us/ENR/Select/Download/1

Describing file columns:

http://electionresults.sos.state.mn.us/ENR/Select/DownloadFileFormats/1



This file gets the results for all elections.
"""
import re
import scraperwiki
import csv
import datetime
import calendar
import logger

# Set up logger
log = logger.ScraperLogger('scraper_results').logger
log.info('[scraper] Scraping general Results data tables.')

urls = {
  'presidential': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/1?mediafileid=22',
  'us_senate': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/1?mediafileid=23',
  'us_house': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/1?mediafileid=24',
  'state_senate': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/1?mediafileid=30',
  'state_house': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/1?mediafileid=20',
  'amendments': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/1?mediafileid=66',
  'supreme_appeal_courts': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/1?mediafileid=37',
  'district_courts': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/1?mediafileid=44',
  'county': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/1?mediafileid=88',
  'municipal': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/1?mediafileid=1',
  'school_board': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/1?mediafileid=7',
  'hospital': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/1?mediafileid=90'
}

# Check for questions.  Only need check once
questionable = False
questions_found = 0
table = scraperwiki.sqlite.select("name FROM sqlite_master WHERE type='table' AND name='meta_questions'")
if table != []:
  questionable = True

# Start scraping
for u in urls:
  
  try:
    data = scraperwiki.scrape(urls[u])
    candidates = csv.reader(data.splitlines(), delimiter=';', quotechar='|')
  except Exception, err:
    log.exception('[%s] Error when trying to read URL and parse CSV: %s' % (u, urls[u]))
    raise
      
  count = 0
  # Make a UTC timestamp
  timestamp = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

  for row in candidates:
    # To better match up with other data, we set a no county_id to 88 as
    # that is what MN SoS uses
    if not row[1] and u in ['amendments', 'us_senate', 'us_house', 'supreme_appeal_courts']:
      row[1] = '88'
      
    # Create ids
    cand_name_id = re.sub(r'\W+', '', row[7])
    office_name_id = re.sub(r'\W+', '', row[4])
    base_id = 'id-' + row[1] + '-' + row[2] + '-' + row[5] + '-' + row[3]
    row_id = base_id + '-' + row[6]
    id_name = base_id + '-' + row[6] + '-' + office_name_id + '-' + cand_name_id
    race_id = base_id
    race_id_name = base_id + '-' + office_name_id
    
    # Attempt to get questions
    question_body = ''
    if questionable:
      question = scraperwiki.sqlite.select("question_body FROM meta_questions WHERE results_id='%s'" % race_id)
      if question != []:
        question_body = question[0]['question_body']
        questions_found = questions_found + 1

    data = {
      'id': row_id,
      'office_type': u,
      'state': row[0],
      'county_id': row[1],
      'precinct_id': row[2],
      'office_id': row[3],
      'office_name': row[4],
      'district_code': row[5], # District, mcd, or fips code
      'candidate_id': row[6],
      'candidate': row[7],
      'suffix': row[8],
      'incumbent_code': row[9],
      'party_id': row[10],
      'precincts_reporting': int(row[11]),
      'total_effected_precincts': int(row[12]),
      'votes_candidate': int(row[13]),
      'percentage': float(row[14]),
      'total_votes_for_office': int(row[15]),
      'id_name': id_name,
      'race_id': race_id,
      'race_id_name': race_id_name,
      'cand_name_id': cand_name_id,
      'office_name_id': office_name_id,
      'question_body': question_body,
      'updated': int(timestamp)
    }
    
    try:
      scraperwiki.sqlite.save(unique_keys = ['id'], data = data, table_name = 'results_general')
      count = count + 1
    except Exception, err:
      log.exception('[%s] Error thrown while saving to database: %s' % (u, data))
      raise

  # Output total for each category
  log.info('[%s] Total rows: %s' % (u, count))


# Note questions found
log.info('[scraper] Questions found: %s' % (questions_found))

# Update some vars for easy retrieval
scraperwiki.sqlite.save_var('updated', int(calendar.timegm(datetime.datetime.utcnow().utctimetuple())))
# Get number of races
races = scraperwiki.sqlite.select("COUNT(DISTINCT race_id) AS race_count FROM results_general")
if races != []:
  scraperwiki.sqlite.save_var('races', races[0]['race_count'])
# Use the presidential race to get a precincts reporting number
p_race = scraperwiki.sqlite.select("* FROM results_general WHERE race_id = 'id----0101'")
if p_race != []:
  scraperwiki.sqlite.save_var('precincts_reporting', p_race[0]['precincts_reporting'])
  scraperwiki.sqlite.save_var('total_effected_precincts', p_race[0]['total_effected_precincts'])


# Let the logger know we are done.
log.info('[scraper] Done scraping general Results data tables.')