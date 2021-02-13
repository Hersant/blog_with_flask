import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
	connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts(title, content) VALUES(?, ?)",
	("Getting started with Flask", "Learn the basics of Flask framework"))

cur.execute("INSERT INTO posts(title, content) VALUES(?,?)",
	("Quick start SQLite", "Learn SQLite in few minutes"))

connection.commit()
connection.close()

