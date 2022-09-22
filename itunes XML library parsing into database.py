import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('tracksdb101.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Album (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id INTEGER,
    title TEXT UNIQUE
);

CREATE TABLE Track (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    Title TEXT UNIQUE,
    album_id INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')

fname = input('Enter file name: ')
if len(fname) < 1: fname = 'Library.xml'

# def lookup101(d, key):
    # if child.tag != 'key' and child.text != key: continue
    # for child in d:
        # return child.text
def lookup(d, key):
    found = False
    for child in d:
        if found: return child.text
        if child.tag == 'key' and child.text == key:
            found = True
    return None


stuff = ET.parse(fname)
all101 = stuff.findall('dict/dict/dict')
print('Dict Count:', len(all101))
for entry in all101:
    if (lookup(entry, 'Track ID')) is None: continue
    name = lookup(entry, 'Name')
    artist = lookup(entry, 'Artist')
    album = lookup(entry, 'Album')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')

    if name is None or artist is None or album is None: continue

    print(name, artist, album, count, rating, length)

    cur.execute('INSERT OR IGNORE INTO Artist (name) VALUES (?)', (artist, ))
    cur.execute('SELECT id FROM Artist WHERE name = ?', (artist, ))
    artist_id = cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO Album (title, artist_id) VALUES (?, ?)', (album, artist_id))
    cur.execute('SELECT id FROM Album WHERE title = ?', (album, ))
    album_id = cur.fetchone()[0]

    cur.execute(''''INSERT OR IGNORE INTO Track (title, album_id, len, rating, count)
    VALUES (?, ?, ?, ?, ?)''', (name, album_id, length, rating, count))

    conn.commit()

# SQL query:
# SELECT Track.title, Album.title, Artist.name
# FROM Track JOIN Album JOIN Artist
# ON Track.album_id = Album.id
# AND Album.artist_id = Artist.id
