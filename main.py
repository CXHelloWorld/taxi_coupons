#!/usr/bin/python

import httplib
import time
import json
import sys
import os

if (len(sys.argv) < 2):
	print "Need url as parameter"
	print "Usage : " + sys.argv[0] + " url "
	sys.exit()

origin_url = sys.argv[1]
print "[ INF ] Url = " + origin_url
if ( not origin_url.startswith("http://")):
	print "[ ERR ] Url Error"
	sys.exit()

url = origin_url[origin_url.index("http://") + len("http://"):]

domain = url[:url.index("/")]
url = url[url.index("/"):]
# print "Domain = " + domain
# print "Url = " + url

if ( not os.path.exists("taxi_coupon.conf")):
	print "[ ERR ] taxi_coupon.conf not found, please write one number per line in taxi_coupon.conf"
	sys.exit()

file = open("taxi_coupon.conf")
while 1:
	number = file.readline();
	if not number:
		break

	number = number.strip('\n')
	# print number, len(number)
	if (len(number) != 11):
		print "[ ERR ] Number " + number + " was not a phone number!"
		continue

	conn = httplib.HTTPConnection(domain)
	conn.request('GET',url)
	result = conn.getresponse()
	resultStatus = result.status
	# print "Respone =", resultStatus
	content = result.read()
	# conn.close()

	token_prefix = 'type=\"hidden\" name=\"token\" id=\"token\" value=\"'
	token = content[content.index(token_prefix) + len(token_prefix):]
	token = token[:token.index("\"")]
	# print "token = " + token

	uuid_prefix = 'type=\"hidden\" name=\"uuid\" id=\"uuid\"  value=\"'
	uuid = content[content.index(uuid_prefix) + len(uuid_prefix):]
	uuid = uuid[:uuid.index("\"")]
	# print "uuid = " + uuid

	shareType_prefix = 'type=\"hidden\" name=\"shareType\" id=\"shareType\"  value=\"'
	shareType = content[content.index(shareType_prefix) + len(shareType_prefix):]
	shareType = shareType[:shareType.index("\"")]
	# print "shareType = " + shareType

	# request coupon
	print "[ INF ] Number = " + number
	coupon_url = "/taxi/web/p/share/apply_gift_package_voucher.htm?uuid=" + uuid \
		+ "&token=" + token + "&shareType=" + shareType
	coupon_url = coupon_url + "&mobile=" + number + "&_=" + bytes(int (time.time() * 1000));
	# print coupon_url

	# conn = httplib.HTTPConnection(domain)
	headers={ "Accept":"*/*", \
		"Accept-Encoding":"gzip, deflate", \
		"Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6", \
		"Connection":"keep-alive", \
		"Content-Length":"0", \
		"Content-Type":"application/x-www-form-urlencoded", \
		"Host":domain, \
		"Origin":"http://" + domain, \
		"Referer":origin_url, \
		"User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36", \
		"X-Requested-With":"XMLHttpRequest" }
	# print headers
	conn.request('POST', coupon_url, headers = headers)
	respones = conn.getresponse()
	resultStatus = respones.status
	# print "Respone =", resultStatus
	content = respones.read()
	conn.close()
	# print content
	if (resultStatus == 200):
		try:
			json_content = json.loads(content);
			if (json_content["code"] == 0):
				print "[ INF ] Get coupon : " + json_content["parameters"]["presentValue"];
			elif (json_content["code"] == 3):
				print "[ INF ] You have already get : " + json_content["parameters"]["presentValue"];
			else:
				print "[ ERR ] Failed because : " + json_content["msg"];
		except:
			print "[ ERR ] Server returned error page : " + content
	else:
		print "[ INF ] Server returned error status : " + resultStatus

	# print content
	# print respones.getheaders();


	# conn.requeset('POST','url',headers=headers)
	# params=urllib.urlencode({'key':'value'});
	# conn.request('POST','url',body=params)