from __future__ import division

import urllib2
import time
import json
import csv
import datetime
import math

yesterdays_date=datetime.date.today()-datetime.timedelta(1)
box_date=yesterdays_date.strftime("%m/%d/%Y")
