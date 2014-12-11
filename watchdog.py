#!/usr/bin/python

import taxi_coupons
import os, shutil
import logging
import time

watch_dir = "."
old_dir = "./old"

logging.basicConfig(level = logging.DEBUG,
	format = '[ %(asctime)s %(levelname)s ] %(message)s',
	filename = 'watchdog.log',
	filemode = 'a')

logging.info("watchdog start running")

while 1:
	print "run"
	try:
		for filename in os.listdir(watch_dir):
			if ( not filename.endswith('.txt')):
				continue

			try:
				fp = open(watch_dir + "/" + filename);
				file_content = fp.read();
				if (file_content.find("http://") > 0):
					url = file_content[file_content.index("http://"):];
					url = url[:url.index("]]")].strip('\n').strip(' ');
					logging.info("Find url in " + filename + ", url = " + url);
					# taxi_coupons.getCoupons(url)
				else:
					logging.info("A boring message in " + filename);
				fp.close();
				shutil.move(watch_dir + "/" + filename, old_dir + "/" + filename);
			except Exception, e:
				raise
	except Exception, e:
		logging.info("watchdog runs into a unexcepted exception")
		raise
	time.sleep(5);