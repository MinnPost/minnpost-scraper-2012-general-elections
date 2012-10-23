# MN 2012 General Election Results

Scraper for the 2012 general election in Minnesota.  Main
results page can be found here:

http://electionresults.sos.state.mn.us/enr/ENR/Home/1
http://electionresults.sos.state.mn.us/ENR/Select/Download/1

## Scraper on Scraperwiki

https://box.scraperwiki.com/zzolo/mn-2012-election-results

## Local setup

Make a virtualenv.

  pip install -r requirements_local.txt 
  
This is used locally to get around some bugs in the scraperwiki 
libraries.

## Independent Deployment

For election night, the scraper needs to run every 10 minutes or less,
and with ScraperWiki, it is not fast enough and there were some issues
with SQLite performance.