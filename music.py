import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('sqlmdb.sqlite')
cur = conn.cursor()

# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    genre   TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    genre_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')


fname = input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'Library.xml'

def lookup(d, key):
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == key :
            found = True
    return None

stuff = ET.parse(fname)
all = stuff.findall('dict/dict/dict')
print('Dict count:', len(all))

for entry in all:
    if ( lookup(entry, 'Track ID') is None ) : continue

    title = lookup(entry, 'Name')
    genre = lookup(entry, 'Genre')
    artist = lookup(entry, 'Artist')
    album = lookup(entry, 'Album')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')

    if title is None or genre is None or artist is None or album is None :
        continue

print(title, genre, artist, album, count, rating, length)

cur.execute('''INSERT OR IGNORE INTO Artist (name)
        VALUES ( ? )''', ( artist, ) )
cur.execute('SELECT id FROM Artist WHERE name = ? OR name IS NULL', (artist, ))
artist_id = cur.fetchone()[0]

cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id )
        VALUES ( ?, ? )''', (album, artist_id))
cur.execute('SELECT id FROM Album WHERE title = ? OR title IS NULL', (album, ))
album_id = cur.fetchone()[0]

cur.execute('''INSERT OR IGNORE INTO Genre (genre)
    VALUES ( ? )''', ( genre, ) )
cur.execute('SELECT id FROM Genre WHERE genre = ? OR genre IS NULL', (genre, ))
genre_id = cur.fetchone()[0]

cur.execute('''INSERT OR REPLACE INTO Track
        (title, album_id, len, rating, count, genre_id)
        VALUES ( ?, ?, ?, ?, ?, ?)''',
        (title, album_id, length, rating, count, genre_id))

conn.commit()
