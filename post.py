#!/usr/bin/python

import cgi
import cgitb
import sqlite3
import sys

cgitb.enable() 

data = cgi.FieldStorage()
player1=data.getfirst('player1')
player2=data.getfirst('player2')
player3=data.getfirst('player3')
player4=data.getfirst('player4')
player5=data.getfirst('player5')

year=data.getfirst('year')

season=data.getfirst('type')

efficiency=data.getfirst('efficiency')

quarter=data.getfirst('quarter')

con=sqlite3.connect('2013_shot_data.db')
cur=con.cursor()
cur.execute("SELECT shot_made_flag FROM test WHERE player_name='Dirk Nowitzki'")
rows=cur.fetchall()



print "Content-Type: text/html\n\n"
print rows