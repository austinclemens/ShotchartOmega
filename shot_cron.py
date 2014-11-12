from __future__ import division

import urllib2
import time
import json
import csv
import datetime
import math
import re
import MySQLdb

yesterdays_date=datetime.date.today()-datetime.timedelta(1)
box_date=yesterdays_date.strftime("%Y%m%d")

url="http://www.nba.com/gameline/%s/" % (box_date)
box_list=urllib2.urlopen(url).read()

find_box=re.compile('nbaGL([0-9]{10})')

boxes=find_box.findall(box_list)
master_shots=[]

for box in boxes:
	game=box
	season="20"+box[3:5]
	if box[2]=="2":
		seasontype="Regular Season"
	if box[2]=="4":
		seasontype="Playoffs"
	nba_call_url='http://stats.nba.com/stats/shotchartdetail?Season=%s&SeasonType=%s&TeamID=0&PlayerID=0&GameID=%s&Outcome=&Location=&Month=0&SeasonSegment=&DateFrom=&Dateto=&OpponentTeamID=0&VsConference=&VsDivision=&Position=&RookieYear=&GameSegment=&Period=0&LastNGames=0&ContextMeasure=FGA' % (season,seasontype,game)
		plays=urllib2.urlopen(nba_call_url)
		data=json.load(plays)
		teams=list(set([row[6] for row in data['resultSets'][0]['rowSet']]))
		for row in data['resultSets'][0]['rowSet']:
			# (player, offense team, defense team, 3pt, made, year, regular/post (0/1), quarter, second remaining, x, y)
			three=0
			if row[12]=='3PT Field Goal':
				three=1
			if row[6]==teams[0]:
				temp=[row[3],teams[0],teams[1],three,row[20],season,0,row[7],row[8]*60+row[9],row[17],row[18]]
			if row[6]==teams[1]:
				temp=[row[3],teams[1],teams[0],three,row[20],season,0,row[7],row[8]*60+row[9],row[17],row[18]]
			master_shots.append(row)

for row in master_shots:
	og
		