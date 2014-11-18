#!/usr/bin/python
import cgi
import MySQLdb
import json

def update_players(year,field):
	if year!='career':
		con=MySQLdb.connect(user='austinc_shotchar', passwd='scriptpass1.', host='localhost', db='austinc_allshotdata')
		cur=con.cursor()
		if field==1:
			cur.execute("""SELECT DISTINCT player FROM shots WHERE year=%s ORDER BY player""" % (year))
		if field==0:
			cur.execute("""SELECT DISTINCT offense_team FROM shots WHERE year=%s ORDER BY offense_team""" % (year))

		names=cur.fetchall()
		con.close()

		return names

	if year=='career':
		con=MySQLdb.connect(user='austinc_shotchar', passwd='scriptpass1.', host='localhost', db='austinc_allshotdata')
		cur=con.cursor()
		cur.execute("""SELECT DISTINCT player FROM shots WHERE year!=1996 ORDER BY player""")
		
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