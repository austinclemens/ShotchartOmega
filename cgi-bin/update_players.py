#!/usr/bin/python
from __future__ import division
import cgi
import MySQLdb
import math
import csv
import cgitb
import json

cgitb.enable()

def update_players(year):
	con=MySQLdb.connect(user='austinc_shotchar', passwd='scriptpass1.', host='localhost', db='austinc_allshotdata')
	cur=con.cursor()
	cur.execute("""SELECT DISTINCT player FROM shots WHERE year=%s""" % (year))

	names=cur.fetchall()
	con.close()

	return names

data = cgi.FieldStorage()
year = data.getfirst('year')

if year==None:
	year=2014

menu_text = update_players(year)

final = json.dumps(menu_text)

print "Content-Type: text/html\n\n"
print final