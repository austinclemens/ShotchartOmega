#!/usr/bin/python
from __future__ import division
import cgi
import MySQLdb
import math
import csv
import cgitb
import json

cgitb.enable()

def update_players(year,field):
	con=MySQLdb.connect(user='austinc_shotchar', passwd='scriptpass1.', host='localhost', db='austinc_allshotdata')
	cur=con.cursor()
	if field==1:
		cur.execute("""SELECT DISTINCT player FROM shots WHERE year=%s""" % (year))
	if field==0:
		cur.execute("""SELECT DISTINCT offense_team FROM shots WHERE year=%s""" % (year))

	names=cur.fetchall()
	con.close()

	return names

data = cgi.FieldStorage()
year = data.getfirst('year')
pl = data.getfirst('pl')

if year==None:
	year=2014

menu_text = update_players(year,int(pl))

final = json.dumps(menu_text)

print "Content-Type: text/html\n\n"
print final