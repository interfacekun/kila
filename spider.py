# -*- coding: utf-8 -*-
##[[
 # @brief:		spider.py

 # @author:		kun si
 # @email:	  	627795061@qq.com
 # @date:		2017-11-07
##]]
import urllib  
import urllib2
import re
import time
import chardet
from dao import Dao

class Spider():

	def __init__(self):
		self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
		self.headers = {'User-Agent':self.user_agent}
		self.dao = Dao()
		self.dao.connect()

	def POST(self, url, headers = None, data = {}):
		headers = headers or self.headers
		try:

			if data:
				data = urllib.urlencode(data)

			request = urllib2.Request(url, data, headers)
			response = urllib2.urlopen(request, timeout = 30)
			page = response.read()
			return page
		except urllib2.URLError, e:
			print e.reason
			return None

	def GET(self, url, headers = None, data = {}):
		headers = headers or self.headers
		try:

			if data :
				dataStr = urllib.urlencode(data)
				url = url + "?" + dataStr
				print(url)

			request = urllib2.Request(url,headers = headers)
			response = urllib2.urlopen(request, timeout = 30)
			page = response.read()
			return page
		except urllib2.URLError, e:
			print e.reason
			return None

	def spiderUrl(self, url, reString, headers = None, data = {}):
		page = self.GET(url)
		pattern = re.compile(reString)
		return re.finditer(pattern, page)

	def spiderPage(self, page, reString):
		pattern = re.compile(reString)
		return re.finditer(pattern, page)

	def getArtistMuisc(self, url, artist, headers = None, data = {}):
		page = self.GET(url)
		if isinstance(artist, unicode):
			artist = artist.encode('utf-8')
		reString = r'<a href="/.*/index_(\d*).html">尾页</a>'
		if type(page) == type('a'):
			results = re.search(re.compile(reString, re.S), page)
			if results :
					maxPage = int(results.group(1))
					print("maxPage %d" % (maxPage))
					for i in range(1, maxPage+1):
						tempUrl = url
						if i != 1:
							tempUrl = url + 'index_' + str(i) + '.html'
						print("[spider url]: %s" % (tempUrl))
						self.getPageMusicUrl(artist, page = None, url = tempUrl)
			else:
				self.getPageMusicUrl(artist, page)

	def getMusicUrl(self, url, title, musicName, artist):
		page = self.GET(url)
		if type(page) == type('a') :
			reString1 = r'''<a href="(http://pan.baidu.com/.*)" title=".*" rel="nofollow" target="_blank" class="blue a_none"><h2 class="bg_gr b_b_s m_s logo mt_1 yh white" style=".*">高速下载</h2></a>'''
			tempResult1 = self.spiderPage(page, reString1)
			panUrl = None
			pwd = None

			for tempM in tempResult1:
				print(tempM.group(1))
				panUrl = tempM.group(1)

			reString2 = r'''<b class="mt_1 yh d_b" style=".*">提取<em class="dn"></em>密码：(.*)</b>'''
			tempResult2 = self.spiderPage(page, reString2)

			for tempM in tempResult2:
				print(tempM.group(1))
				pwd = tempM.group(1)
			print("----------A---------")
			return panUrl, pwd

	def getPageMusicUrl(self, artist, page = None, url = None, reString = None):
		reString = reString or r'<a href="(http://www.51ape.com/ape/\d*.html)" class="wm210 c3b fl f_14 over t20d ml_1" title="(%s.*)">(.*)</a>' % (artist)
		if not page:
			page = self.GET(url)

		if type(page) == type('a'):
			results = self.spiderPage(page, reString)
			i = 1
			for m in results:
				tempUrl = m.group(1)
				title = m.group(2)
				musicName = m.group(3)

				panUrl, pwd = self.getMusicUrl(tempUrl,title, musicName, artist)

				print("title:%s" % (title))
				print("musicName:%s" % (musicName))
				print("artist:%s" % (artist))
				
				self.dao.saveMusic(title, musicName, artist, panUrl, pwd)
				
				time.sleep(1)
				
				print("page %d music" % (i))
				i = i + 1

			print("[total] %d" % (i-1))
	def getMusic(self, sql, args = None):
		musicList = self.dao.launchSQL(sql, args)
		i = 0
		content = ""
		for row in musicList:
			i = i + 1
			musicName = row[2]
			url = row[4]
			pwd = row[5]

			try:
				content = content + "歌曲名：%s\n百度云盘下载地址：\n%s\n密码：%s\n\n" % (musicName.encode("utf-8"), url.encode("utf-8"), pwd.encode("utf-8"))
			except Exception as e:
				print e

		if i == 0:
			content = "不好意思程序员有点菜，没找到这首歌!"
			print content
		else:
			print content
			
	def getInstagramAsset(self, page = None, url = None, reString = None):
		if not page:
			page = self.GET(url)
		if type(page) == type('a'):
			reString = reString or r'"(https://scontent-sin6-2.cdninstagram.com/[^{]*?/\w750x750/.*?)"'
			results = re.finditer(re.compile(reString), page)
			return results


if __name__ == '__main__':
	spider = Spider()
	# url = "http://www.baidu.com/"
	# data = {"name":"123", "pwd":"123"}
	# page = spider.GET(url, None, data)
	# print(page)
	# url = "http://www.51ape.com/artist/"
	# reString = r'<div class="gs_a"><a href="(http://www.51ape.com/\w*/)" class="c47 f_14 b yh">(.*)</a></div>'
	# spider.spiderUrl(url, reString)
	# url = "http://www.51ape.com/jay/"
	# spider.getArtistMuisc(url, "周杰伦")
	# dao = Dao()
	# dao.connect()
	# muiscName = "退后"
	# sql = "select * from music where `musicName` like %s limit 10;"
	# args = ('%%%s%%' % muiscName)
	# musicList = dao.launchSQL(sql, args)
	# if musicList:
	# 	for row in musicList:
	# 		musicName = row[2]
	# 		artist = row[3]
	# 		url = row[4]
	# 		pwd = row[5]
	# 		try:
	# 			content = "歌曲名：%s\n歌手：%s\n百度云盘下载地址：%s\n密码：%s" % (musicName.encode("utf-8"), artist.encode("utf-8"), url.encode("utf-8"), pwd.encode("utf-8"))
	# 			print content
	# 		except Exception as e:
	# 			print e
	# content = "歌手 周杰伦"
	# reString = r' '
	# results = re.split(re.compile(reString), content)
	# if results:
	# 	if results[0] == "歌手":
	# 		artist = results[1]
	# 		print "artist", artist
	# 		if len(results) == 3 and results[2]:
	# 			page = int(results[2])
	# 			start = (page-1)*5+1
	# 			end = page*5
	# 			sql = "select * from music where `artist` like '%s%%' "; 
	# 			sql = sql % artist
	# 			sql = sql + "limit %d, %d;" % (start, end)
	# 			spider.getMusic(sql)
	# 		else:
	# 			sql = "select * from music where `artist` like %s limit 5;"
	# 			args = ('%s%%' % artist)
	# 			print(args)
	# 			spider.getMusic(sql, args)
	# 			
	url = "https://www.instagram.com/p/Bbf6cNOnolj/"
	spider.getInstagramAsset(None, url)