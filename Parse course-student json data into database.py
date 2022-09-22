import json
import sqlite3

conn = sqlite3.connect('test_roster101.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Course(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE
);

CREATE TABLE Member(
    user_id INTEGER,
    course_id INTEGER,
    role INTEGER,
    PRIMARY KEY(user_id, course_id)
)
''')

fname = input('Enter file name: ')
if len(fname) < 1:
    fname = 'roster_data_sample.json'

stuff = open(fname).read()
stuff101 = json.loads(stuff)
print(len(stuff101))

for line in stuff101:
    user = line[0]
    course = line[1]
    role = line[2]

print(user, course, role)

cur.execute('INSERT OR IGNORE INTO User (name) VALUES (?)', (user,))
cur.execute('SELECT id FROM User WHERE name = ?', (user,))
user_id = cur.fetchone()[0]

cur.execute('INSERT OR IGNORE INTO Course (title) VALUES (?)', (course,))
cur.execute('SELECT id FROM Course WHERE title = ?', (course,))
course_id = cur.fetchone()[0]

cur.execute('''
    INSERT OR REPLACE INTO Member(user_id, course_id, role)
    VALUES(?, ?, ?)''', (user_id, course_id, role))

conn.commit()

# SQL Query:
# SELECT User.name, Member.role, Course.title
# FROM User JOIN Member JOIN Course
# ON Member.user_id = User.id
# AND Member.course_id = Course.id
# ORDER BY User.name, Course.title, Member.role DESC
