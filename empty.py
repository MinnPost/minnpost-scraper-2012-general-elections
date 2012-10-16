"""
Empties database.  Use with caution.
"""
import scraperwiki
import sqlite3
import dumptruck

dt = dumptruck.DumpTruck(dbname='scraperwiki.sqlite')

print 'Dropping all tables ...'
stables = scraperwiki.sqlite.show_tables()
print stables
tables = dt.tables()
for t in tables:
  print 'Dropping %s ...' % t
  dt.drop(t)