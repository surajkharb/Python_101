import sqlite3

conn = sqlite3.connect('test101.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

fname = input('Enter file name: ')
if len(fname) < 1: fname = 'mbox.txt'
fopen = open(fname)

for line in fopen:
    if not line.startswith('From: '): continue
    list101 = line.split()
    email = list101[1].split('@')
    email_ext = email[1]
    # print(email_ext)
    cur.execute('SELECT count FROM Counts WHERE org = ?', (email_ext,))
    count101 = cur.fetchone()
    if count101 is None:
        cur.execute('INSERT INTO Counts (org, count) VALUES (?, 1)', (email_ext,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (email_ext,))
    conn.commit()

top = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 1'
cur.execute(top)
top_result = cur.fetchone()
print(top_result[0], top_result[1])

cur.close()
