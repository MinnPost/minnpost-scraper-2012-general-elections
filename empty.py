"""
Empties database.  Use with caution.
"""
import scraperwiki

print 'Emptying database (all tables) ...'
scraperwiki.sqlite.execute('DELETE FROM swdata;', verbose=1)