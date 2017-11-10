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
                    reString = r'歌曲 (.*)'
                    results = re.search(re.compile(reString), content)
                    if results:
                        if results.group(1):
                            muiscName = results.group(1)
                            if isinstance(muiscName, unicode):
                                print "123"
                                muiscName = muiscName.encode('utf-8')
                            print muiscName
                            sql = "select * from music where `musicName` like %s limit 5;"
                            args = ('%%%s%%' % muiscName)
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
                                print content
                                replyMsg = reply.TextMsg(toUser, fromUser, content)
                                return replyMsg.send()
                            if i == 0:
                                content = "不好意思程序员有点菜，没找到这首歌!"
                                replyMsg = reply.TextMsg(toUser, fromUser, content)
                                return replyMsg.send()
                    else:
                        reString = r'歌手 (.*) (.*)'
                        results = re.search(re.compile(reString), content)
                        if results:
                            if results.group(1):
                                if results.group(2):
                                    page = int(results.group(2))
                                    sql = "select * from music where `artist` like %s;"
                                    args = ('%%%s%% limit %d, %d' % (artist, (page-1)*5+1, page*5))
                                    musicList = self.dao.launchSQL(sql, args)
                                    content = ""
                                    for row in musicList:
                                        musicName = row[2]
                                        artist = row[3]
                                        url = row[4]
                                        pwd = row[5]
                                        try:
                                            content = content + "歌曲名：%s\n百度云盘下载地址：\n%s\n密码：%s\n\n" % (musicName.encode("utf-8"), artist.encode("utf-8"), url.encode("utf-8"), pwd.encode("utf-8"))
                                        except Exception as e:
                                            print e
                                    print content
                                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                                    return replyMsg.send()
                                else:
                                    sql = "select * from music where `artist` like %s limit 5;"
                                    args = ('%%%s%%' % artist)
                                    musicList = self.dao.launchSQL(sql, args)
                                    content = ""
                                    for row in musicList:
                                        musicName = row[2]
                                        artist = row[3]
                                        url = row[4]
                                        pwd = row[5]
                                        try:
                                            content = content + "歌曲名：%s\n百度云盘下载地址：\n%s\n密码：%s\n\n" % (musicName.encode("utf-8"), artist.encode("utf-8"), url.encode("utf-8"), pwd.encode("utf-8"))
                                        except Exception as e:
                                            print e
                                    print content
                                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                                    return replyMsg.send()
                            else:
                                content = "不好意思程序员有点菜，没有收录该艺术家的歌曲!"
                                replyMsg = reply.TextMsg(toUser, fromUser, content)
                                return replyMsg.send()
                        else:
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