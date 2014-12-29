#!/usr/bin/python

from xml.etree import ElementTree

# text
# <xml>
# <ToUserName><![CDATA[toUser]]></ToUserName>
# <FromUserName><![CDATA[fromUser]]></FromUserName> 
# <CreateTime>1348831860</CreateTime>
# <MsgType><![CDATA[text]]></MsgType>
# <Content><![CDATA[this is a test]]></Content>
# <MsgId>1234567890123456</MsgId>
# </xml>

# picture
# <xml>
# <ToUserName><![CDATA[toUser]]></ToUserName>
# <FromUserName><![CDATA[fromUser]]></FromUserName>
# <CreateTime>1348831860</CreateTime>
# <MsgType><![CDATA[image]]></MsgType>
# <PicUrl><![CDATA[this is a url]]></PicUrl>
# <MediaId><![CDATA[media_id]]></MediaId>
# <MsgId>1234567890123456</MsgId>
# </xml>

# voice
# <xml>
# <ToUserName><![CDATA[toUser]]></ToUserName>
# <FromUserName><![CDATA[fromUser]]></FromUserName>
# <CreateTime>1357290913</CreateTime>
# <MsgType><![CDATA[voice]]></MsgType>
# <MediaId><![CDATA[media_id]]></MediaId>
# <Format><![CDATA[Format]]></Format>
# <MsgId>1234567890123456</MsgId>
# </xml>

# video
# <xml>
# <ToUserName><![CDATA[toUser]]></ToUserName>
# <FromUserName><![CDATA[fromUser]]></FromUserName>
# <CreateTime>1357290913</CreateTime>
# <MsgType><![CDATA[video]]></MsgType>
# <MediaId><![CDATA[media_id]]></MediaId>
# <ThumbMediaId><![CDATA[thumb_media_id]]></ThumbMediaId>
# <MsgId>1234567890123456</MsgId>
# </xml>

# location
# <xml>
# <ToUserName><![CDATA[toUser]]></ToUserName>
# <FromUserName><![CDATA[fromUser]]></FromUserName>
# <CreateTime>1351776360</CreateTime>
# <MsgType><![CDATA[location]]></MsgType>
# <Location_X>23.134521</Location_X>
# <Location_Y>113.358803</Location_Y>
# <Scale>20</Scale>
# <Label><![CDATA[LocationMessage]]></Label>
# <MsgId>1234567890123456</MsgId>
# </xml>

# link
# <xml>
# <ToUserName><![CDATA[toUser]]></ToUserName>
# <FromUserName><![CDATA[fromUser]]></FromUserName>
# <CreateTime>1351776360</CreateTime>
# <MsgType><![CDATA[link]]></MsgType>
# <Title><![CDATA[LINK]]></Title>
# <Description><![CDATA[LINK]]></Description>
# <Url><![CDATA[url]]></Url>
# <MsgId>1234567890123456</MsgId>
# </xml>

# subscribe
# <xml>
# <ToUserName><![CDATA[toUser]]></ToUserName>
# <FromUserName><![CDATA[FromUser]]></FromUserName>
# <CreateTime>123456789</CreateTime>
# <MsgType><![CDATA[event]]></MsgType>
# <Event><![CDATA[subscribe]]></Event>
# </xml>

class wx_msg(object):
	"""docstring for wx_msg"""
	def __init__(self):
		super(wx_msg, self).__init__()

	def parseFromXMLString(self, xmlString):
		root = ElementTree.fromstring(xmlString)
		self.toUserName = root.find("ToUserName").text
		self.fromUserName = root.find("FromUserName").text
		self.createTime = root.find("CreateTime").text
		self.msgType = root.find("MsgType").text

		if (self.msgType == "event"):
			self.event = root.find("Event").text
			self.eventKey = root.find("EventKey").text

		if (self.msgType == "text"):
			self.content = root.find("Content").text
			self.msgId = root.find("MsgId").text

	def parseFromXMLFile(self, xmlFile):
		self.parseFromXMLString(open(xmlFile).read())