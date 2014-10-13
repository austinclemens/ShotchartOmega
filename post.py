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

con=sqlite3.connect('/home2/austinc/%s_shot_data.db' % (year))
cur=con.cursor()
cur.execute("SELECT * FROM test WHERE player_name='%s'" % (player1))
rows=cur.fetchall()

average_csv=

results_csv=goldsberry(rows,average_csv)

def goldsberry(shots,average_data):
	"""Creates the Goldberry chart (csv) for given player"""
	shots_temp=[['',int(shot[18]),int(shot[17]),int(shot[20]),int(shot[12])] for shot in shots]
	# columns are: blank (for circle_chunk,y_loc,x_loc,shot_made,3pt)
	player_data=circle_chunk2(shots_temp)
	# x_center, y_center, number of shots, number of made shots, region, player name, smoothed fg%, region fg%, relative prop of shots, region shots, region made, total_shots, pps
	csv_data=[]
	for i,region in enumerate(player_data):
		csv_data.append([region[0],region[1],region[2],float(region[3])-float(average_data[i][3]),float(region[3]),region[4],(len([shot for shot in shots_temp if math.sqrt((region[0]+5-shot[1])**2+(region[1]+5-shot[2])**2)<20]))/len(shots_temp),region[5]-averagepps,(len([shot for shot in shots_temp if math.sqrt((region[0]+5-shot[1])**2+(region[1]+5-shot[2])**2)<50]))/len(shots_temp)])
	sorted_chart=sorted(csv_data, key=itemgetter(2,6))
	sorted_chart=sorted_chart[-201:]
	sorted_chart.reverse()
	sorted_chart=[[shot[0],shot[1],shot[2],round(shot[3],4),round(shot[4],4),shot[5],round(shot[6],4),round(shot[7],4),round(shot[8],4)] for shot in sorted_chart]
	return sorted_chart

def circle_chunk2(shots_temp,bin_per=.08,regions=0):
	"""New New chunking routine, to chunk shots into 16 mostly semi-circular zones. Rows come in organized
	as: [p_name,x_loc,y_loc,shot_made,3pt_flag].  It returns 1,500 locations - these are 1 foot x 1 foot. Each
	location in a zone, however, will have the same fg%. Court locations have domain -40 < x < 310 and range
	-250 < y < 250. Returns an output list like so: [sw_x,sw_y,ne_x,ne_y,#shots,fg%,p_name]"""
	total_shots=len(shots_temp)
	bin_size=total_shots*bin_per
	output=[]
	p_name=shots_temp[0][0]
	box_matrix=point_matrix()
	shots_t=0
	for box in box_matrix:
		x_center=box[0][0]+5
		y_center=box[0][1]+5
		shots2=[shot for shot in shots_temp if int(shot[1])>=box[0][0] and int(shot[1])<box[1][0] and int(shot[2])>=box[0][1] and int(shot[2])<box[1][1]]
		num_shots=len(shots2)
		smooth_fg=0
		dists=[]
		dist_shots=[shot for shot in shots_temp]
		dist_shots=[shot for shot in dist_shots if math.sqrt((x_center-shot[1])**2+(y_center-shot[2])**2)<50] 
		for shot in dist_shots:
			dist=math.sqrt((x_center-shot[1])**2+(y_center-shot[2])**2)
			dists.append([dist,shot[3]])
		sorted_dists = sorted(dists, key=lambda place:place[0])
		# fill_shots=sorted_dists[0:int(find_x_shots)]
		fill_shots=sorted_dists
		shots_made_smooth=0
		for shot in fill_shots:
			shots_made_smooth=shots_made_smooth+(shot[1]*(1/sqrt(shot[0])))
		num_shots_smooth=0
		for shot in fill_shots:
			num_shots_smooth=num_shots_smooth+(1/sqrt(shot[0]))
		try:
			smooth_fg=shots_made_smooth/num_shots_smooth
		except: 
			smooth_fg=0
		three_regions=[13,14,15,16,4,5]
		if int(box[2][0]) in three_regions:
			pps_made_smooth=shots_made_smooth*1.5
		if int(box[2][0]) not in three_regions:
			pps_made_smooth=shots_made_smooth
		try: 
			smooth_pps=2*pps_made_smooth/num_shots_smooth
		except:
			smooth_pps=0
		output.append([box[0][0],box[0][1],num_shots,smooth_fg,find_region(box[0][0]+5,box[0][1]+5),smooth_pps])
	return output

print "Content-Type: text/html\n\n"
print results_csv