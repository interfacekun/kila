# -*- coding: utf-8 -*-
# filename: handle.py
import hashlib
import reply
import receive
import web
from robot import Robot
from basic import Basic
from material import Material
from dao import Dao
import re

class Handle(object):
    def __init__(self):
        self.robot = Robot()
        self.basic = Basic()
        self.material = Material()
        self.dao  = Dao()
        self.dao.connect()
    def POST(self):
        try:
            webData = web.data()
            print "Handle Post webdata is ", webData   #后台打日志
            recMsg = receive.parse_xml(webData)
            # accessToken = self.basic.get_access_token()
            # print accessToken
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = recMsg.Content
                try:
                    print content
                    reString = r' '
                    results = re.split(re.compile(reString), content)
                    if results[0] == "歌曲":
                        if len(results) == 2 and results[1]:
                            muiscName = results[1]
                            if isinstance(muiscName, unicode):
                                muiscName = muiscName.encode('utf-8')
                            print muiscName
                            sql = "select * from music where `musicName` like %s limit 5;"
                            args = ('%s%%' % muiscName)
                            musicList = self.dao.launchSQL(sql, args)
                            content = ""
                            i = 0
                            if musicList:
                                for row in musicList:
                                    i = i + 1
                                    musicName = row[2]
                                    artist = row[3]
                                    url = row[4]
                                    pwd = row[5]
                                    try:
                                        content = content + "歌曲名：%s\n歌手：%s\n百度云盘下载地址：\n%s\n密码：%s\n\n" % (musicName.encode("utf-8"), artist.encode("utf-8"), url.encode("utf-8"), pwd.encode("utf-8"))
                                    except Exception as e:
                                        print e
                            if i == 0:
                                content = "不好意思程序员有点菜，没找到这首歌!"
                                replyMsg = reply.TextMsg(toUser, fromUser, content)
                                return replyMsg.send()
                            else:
                                print content
                                replyMsg = reply.TextMsg(toUser, fromUser, content)
                                return replyMsg.send()

                    elif results[0] == "歌手":
                        if len(results) >= 2 and results[1]:
                            artist = results[1]
                            if len(results) == 3 and results[2]:
                                try:
                                    page = int(results[2])
                                    start = (page-1)*5+1
                                    end = 5
                                    sql = "select * from music where `artist` like '%s%%' "; 
                                    sql = sql % artist
                                    sql = sql + "limit %d, %d;" % (start, end)
                                    return self.getMusic(toUser, fromUser,sql)
                                except Exception as e:
                                    print e
                                    musicName = results[2]
                                    sql = "select * from music where `artist` like '%s%%' "; 
                                    sql = sql % artist
                                    sql = sql + "and `musicName` like '%s%%';" % musicName
                                    return self.getMusic(toUser, fromUser,sql)
                            if len(results) == 4 and results[2] == "歌曲" and results[3]:
                                musicName = results[3]
                                sql = "select * from music where `artist` like '%s%%' "; 
                                sql = sql % artist
                                sql = sql + "and `musicName` like '%s%%';" % musicName
                                return self.getMusic(toUser, fromUser,sql)
                            else:
                                sql = "select * from music where `artist` like %s limit 5;"
                                args = ('%s%%' % artist)
                                return self.getMusic(toUser, fromUser,sql, args)
                    content = self.robot.getRobotReply(fromUser, content)
                    print content
                    #content = "嗨，这么巧的!"
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()

                except Exception as e:
                    print("[--erorr--]", e)

            elif isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'image':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                mediaId = recMsg.MediaId
                replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                return replyMsg.send()
            else:
                print "暂且不处理"
                return "success"
        except Exception, Argment:
            return Argment

    def getMusic(self, toUser, fromUser, sql, args = None):
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
            content = "不好意思程序员有点菜，没收录该艺术家的歌曲!"
            replyMsg = reply.TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        else:
            print content
            replyMsg = reply.TextMsg(toUser, fromUser, content)
            return replyMsg.send()