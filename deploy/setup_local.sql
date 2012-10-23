-- This file is used to set up the database locally.  This
-- cannot be performed on Scraperwiki

-- https://www.sqlite.org/wal.html
-- Default is: PRAGMA journal_mode=DELETE;
PRAGMA journal_mode=WAL;