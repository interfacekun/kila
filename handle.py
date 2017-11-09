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
                            sql = "select * from music where `musicName` like %s limit 10;"
                            args = ('%%%s%%' % muiscName)
                            musicList = self.dao.launchSQL(sql, args)
                            if musicList:
                                for row in musicList:
                                    muiscName = row[2]
                                    artist = row[3]
                                    url = row[4]
                                    pwd = row[5]
                                    content = "歌曲名：%s\n歌手：%s\n百度云盘下载地址：%s\n密码：%s" % (musicName, artist, url, pwd)
                                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                                    return replyMsg.send()
                    else:
                        content = self.robot.getRobotReply(fromUser, content)
                        print content
                        #content = "嗨，这么巧的!"
                        replyMsg = reply.TextMsg(toUser, fromUser, content)
                        return replyMsg.send()
                except Exception as e:
                    print("[--erorr--]", e.reason)

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