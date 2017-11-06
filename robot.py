# -*- coding: utf-8 -*-
# filename: robot.py

import json
import urllib
import urllib2
import re
import time

class Robot():
	def __init__(self):
		self.mykey = "2ba52d0c1f3341d18be2e48fc4405b3d"
		self.url = "http://www.tuling123.com/openapi/api"
	def getRobotReply(self, userID, content):
		try:
			json_data = urllib.urlencode({"key":self.mykey,"info":content,"userid":str(userID)})
			fs=urllib2.urlopen(url=self.url, data=json_data)
			result_str = fs.read().decode('utf-8')
			json_resp = json.loads(result_str,encoding="utf-8")
			return json_resp["text"].encode("utf-8")
		except Exception as e:
				print e
				return "对不起，我可能宕机了!"