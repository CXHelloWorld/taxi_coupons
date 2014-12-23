#!/usr/bin/python

import taxi_coupons
import os, shutil
import logging
import time
import datetime
import traceback
from wx_msg import wx_msg

watch_dir = "./new"
old_dir = "./old"

logging.basicConfig(level = logging.DEBUG,
	format = '[ %(asctime)s %(levelname)s ] %(message)s',
	filename = 'watchdog.log',
	filemode = 'a')

logging.info("watchdog start running")

def parseText(content):
	if (content.find("http://") > 0):
		url = content.strip(" ")[content.index("http://"):]
		print url
		logging.info("Find url in " + filename + ", url = " + url);
		resultCodes = taxi_coupons.getCoupons(url)
		count_1 = 0
		for code in resultCodes:
			# print code
			if (code == 1):
				count_1 = count_1 + 1
		if (len(resultCodes) > 0 and count_1 == len(resultCodes)):
			return 1
		else:
			return 0
	else:
		logging.info("A boring message in " + filename);
		return -1

while 1:
	resumeTime = -1;
	try:
		for filename in os.listdir(watch_dir):
			if ( not filename.endswith('.txt')):
				continue

			try:
				msg = wx_msg()
				msg.parseFromXMLFile(watch_dir + "/" + filename)
				if (msg.msgType == "text"):
					res = parseText(msg.content)
					# print res
					if (res == 1):
						# resume at tomorrow 10:00 am
						resumeTime = (int(time.time()) / 86400 + 1) * 86400 + 7200
					else:
						# pass
						shutil.move(watch_dir + "/" + filename, old_dir + "/" + filename);
			except Exception, e:
				logging.info("exception occured when getting coupons");
				logging.error(traceback.format_exc());
				shutil.move(watch_dir + "/" + filename, old_dir + "/" + filename);
	except Exception, e:
		logging.info("watchdog runs into a unexcepted exception")
		logging.error(traceback.format_exc());

	if (resumeTime < 0):
		time.sleep(5);
	else:
		logging.info("All buddies get full coupons today, watchdog will resume at " + bytes(datetime.datetime.fromtimestamp(resumeTime)))
		time.sleep(resumeTime - time.time())