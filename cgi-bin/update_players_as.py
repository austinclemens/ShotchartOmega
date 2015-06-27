#!/usr/bin/python
import cgi
import MySQLdb
import json
import cgitb

cgitb.enable()

def update_players():
	con=MySQLdb.connect(read_default_file="/home/austinc/etc/my.cnf", host='localhost', db='austinc_allshotdata')
	cur=con.cursor()
	cur.execute("""SELECT DISTINCT player FROM `shots` WHERE season_type=3 GROUP BY player HAVING COUNT(*)>50""")

	names=cur.fetchall()
	con.close()

	new_names=[a for a in names]

	return new_names

menu_text = update_players()
final = json.dumps(menu_text)

print "Content-Type: text/html\n\n"
print final