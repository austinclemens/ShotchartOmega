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

def update(box_date):
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
			seasonindicator=0
		if box[2]=="4":
			seasontype="Playoffs"
			seasonindicator=1
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
						temp=[game,row[4],teams[0],teams[1],three,row[20],year,seasonindicator,row[7],row[8]*60+row[9],row[17],row[18]]
				if row[6]==teams[1]:
					temp=[game,row[4],teams[1],teams[0],three,row[20],year,seasonindicator,row[7],row[8]*60+row[9],row[17],row[18]]
				master_shots.append(row)

	con=MySQLdb.connect(user='austinc_shotchar', passwd='scriptpass1.', host='localhost', db='austinc_allshotdata')
	cur=con.cursor()

	for row in master_shots:
		cur.execute("""INSERT INTO shots (gameid,player,offense_team,defense_team,three,made,year,season_type,quarter,seconds_remain,x,y) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11]))

	cur.close()

update(box_date)
get_averages()