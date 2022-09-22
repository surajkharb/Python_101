import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('tracks_test.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Tracks;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;

CREATE TABLE Artist (
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
artist_name TEXT UNIQUE
);

CREATE TABLE Genre(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    genre_name TEXT UNIQUE
);

CREATE TABLE Album(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    album_name TEXT UNIQUE,
    artist_id INTEGER
);

CREATE TABLE Tracks(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    album_id INTEGER,
    genre_id INTEGER
)

''')

fname = input('Enter file name: ')
if (len(fname) < 1): fname = 'Library.xml'


def tuktuk(d, key):
    found = False
    for wheel in d:
        if found: return wheel.text
        if wheel.tag == 'key' and wheel.text == key:
            found = True
    return None


stuff = ET.parse(fname)
trip = stuff.findall('dict/dict/dict')
print('Dict count:', len(trip))
for place in trip:
    # print(111111)
    if tuktuk(place, 'Track ID') is None: continue
    # print(22222)
    track_title = tuktuk(place, 'Name')
    album = tuktuk(place, 'Album')
    artist = tuktuk(place, 'Artist')
    genre = tuktuk(place, 'Genre')

    if track_title is None or artist is None or album is None or genre is None:
        continue

    print(track_title, album, artist, genre)

    cur.execute('INSERT OR IGNORE INTO Artist (artist_name) VALUES (?)', (artist,))
    cur.execute('SELECT id FROM Artist WHERE artist_name = ?', (artist,))
    artist_id = cur.fetchone()[0]

    cur.execute('''
    INSERT OR IGNORE INTO Album(album_name, artist_id)
    VALUES(?, ?)''', (album, artist_id))
    cur.execute('SELECT id FROM Album WHERE album_name = ?', (album,))
    album_id = cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO Genre (genre_name) VALUES (?)', (genre,))
    cur.execute('SELECT id FROM Genre WHERE genre_name = ?', (genre,))
    genre_id = cur.fetchone()[0]

    cur.execute('''
    INSERT
    OR
    IGNORE
    INTO
    Tracks(title, album_id, genre_id)
    VALUES(?, ?, ?)''', (track_title, album_id, genre_id))

    conn.commit()

# SQL Query:
# SELECT Tracks.title, Album.album_name, Artist.artist_name, Genre.genre_name
# FROM Tracks JOIN Album JOIN Artist JOIN Genre
# ON Tracks.album_id = Album.id AND Tracks.genre_id = Genre.id
# AND Album.artist_id = Artist.id
