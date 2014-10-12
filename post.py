#!/usr/bin/python

import cgi
import cgitb
import sqlite3
import sys

cgitb.enable() 

con=sqlite3.connect('2013_shot_data.db')
cur=con.cursor()
cur.execute("SELECT shot_made_flag FROM test WHERE player_name='Dirk Nowitzki'")
rows=cur.fetchall()

data = cgi.FieldStorage()

my_param=data.getfirst('a')

print "Content-Type: text/html\n\n"
print rows