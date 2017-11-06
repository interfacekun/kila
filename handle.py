# -*- coding: utf-8 -*-
# filename: handle.py
import hashlib
import reply
import receive
import web
from robot import Robot
from basic import Basic
from material import Material

class Handle(object):
    def __init__(self):
        self.robot = Robot()
        self.basic = Basic()
        self.material = Material()
    def POST(self):
        try:
            webData = web.data()
            print "Handle Post webdata is ", webData   #后台打日志
            recMsg = receive.parse_xml(webData)
            accessToken = self.basic.get_access_token()
            print accessToken
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = recMsg.Content
                content = self.robot.getRobotReply(fromUser, content)
                print content
                #content = "嗨，这么巧的!"
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                mediaType = "news"
                newsMaterial = self.material.batch_get(accessToken, mediaType)
                print(newsMaterial)
                return replyMsg.send()
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