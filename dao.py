# -*- coding: utf-8 -*-
##[[
 # @brief:		dao.py

 # @author:		kun si
 # @email:	  	627795061@qq.com
 # @date:		2017-11-07
##]]

import pymysql
import chardet

class Dao():

	def __init__(self):
		self.host = "127.0.0.1"
		self.port = "3306"
		self.dbName = "musicApe"
		self.userName = "interface"
		self.password = "627795061"
		self.db = None
		self.cursor = None

	def connect(self, host=None, dbName=None, userName=None, password=None):
		host = host or self.host
		dbName = dbName or self.dbName
		userName = userName or self.userName
		password = password or self.password
		self.db = pymysql.connect(host, userName, password, dbName, charset="utf8")
		self.cursor = self.db.cursor()
		return self.cursor

	def close(self):
		self.db.close()

	def launchSQL(self, sql, args):
		try:
			if args:
				test = self.cursor.execute(sql, args)
			else:
				test = self.cursor.execute(sql)
			self.db.commit()
			results = self.cursor.fetchall()
			return results
		except Exception as e:
			print "sql error", sql, e
			self.db.rollback()

	def saveMusic(self, title, musicName, artist, panUrl, pwd):
		try:
			sql = "insert into music(`title`, `musicName`, `artist`, `url`, `password`) values('%s', '%s', '%s', '%s', '%s');" % (title, musicName, artist, panUrl, pwd)
			self.launchSQL(sql)
		except Exception as e:
			print("save Music fail", e, title, musicName, artist)
			print(chardet.detect(title), chardet.detect(musicName), chardet.detect(artist))

if __name__ == '__main__':
	dao = Dao()
	dao.connect()
	sql = "select * from test;"
	results = dao.launchSQL(sql)
	for row in results:
		for v in row:
			print(v)
	dao.close()