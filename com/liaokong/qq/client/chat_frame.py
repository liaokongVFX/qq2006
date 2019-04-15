# -*- coding: utf-8 -*-
# Time    : 2019/4/14 20:07
# Author  : LiaoKong


"""好友聊天窗口"""
import datetime
import json
import threading

import wx

from com.liaokong.qq.client.my_frame import *


class ChatFrame(MyFrame):
    def __init__(self, friendsframe, user, friend):
        super(ChatFrame, self).__init__(title="", size=(450, 400))

        self.friendsframe = friendsframe
        self.user = user
        self.friend = friend

        title = "{0}与{1}聊天中...".format(user["user_name"], friend["user_name"])

        self.SetTitle(title)

        # 创建消息文本输入控件
        self.seemesg_tx = wx.TextCtrl(self.content_panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.seemesg_tx.SetFont(
            wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName="微软雅黑"))

        # 底部发送消息面板
        bottompanel = wx.Panel(self.content_panel, style=wx.DOUBLE_BORDER)
        bottombox = wx.BoxSizer()

        self.sendmsg_tc = wx.TextCtrl(bottompanel)
        self.sendmsg_tc.SetFont(
            wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName="微软雅黑"))

        # 发送消息按钮
        sendmsg_btn = wx.Button(bottompanel, label="发送")
        self.Bind(wx.EVT_BUTTON, self.on_click, sendmsg_btn)

        bottombox.Add(self.sendmsg_tc, 5, wx.CENTER | wx.ALL | wx.EXPAND, border=5)
        bottombox.Add(sendmsg_btn, 1, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

        bottompanel.SetSizer(bottombox)

        # 创建整体布局
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.seemesg_tx, 5, wx.CENTER | wx.ALL | wx.EXPAND, border=5)
        box.Add(bottompanel, 1, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

        self.content_panel.SetSizer(box)

        # 消息日志
        self.msglog = ""

        # 初始化线程
        # 设置子线程状态
        self.isrunning = True
        # 创建一个子线程
        self.t1 = threading.Thread(target=self.thread_body)
        self.t1.start()

    # 线程方法
    def thread_body(self):
        # 当前线程对象
        while self.isrunning:
            try:
                # 从服务器接收数据
                json_data, _ = client_socket.recvfrom(1024)

                # JSON 解码
                json_obj = json.loads(json_data.decode())
                logger.info("从服务器接收数据：{0}".format(json_obj))

                cmd = json_obj["command"]
                if cmd is not None and cmd == COMMAND_REFRESH:
                    userid_list = json_obj["OnlineUserList"]

                    if userid_list is not None and len(userid_list) > 0:
                        # 刷新好友列表
                        self.friendsframe.refresh_friend_list(userid_list)

                else:
                    # 接收聊天消息
                    now = datetime.datetime.today()
                    strnow = now.strftime("%Y-%m-%d %H:%M:%S")
                    message = json_obj["message"]

                    log = "#{0}\n{1}对您说：{2}\n".format(strnow, self.friend["user_name"], message)
                    self.msglog += log

                    self.seemesg_tx.SetValue(self.msglog)

                    # 光标显示在最后一行
                    self.seemesg_tx.SetInsertionPointEnd()

            except Exception:
                continue

    def on_click(self, event):
        # 发送消息
        if self.sendmsg_tc.GetValue() != "":
            now = datetime.datetime.today()
            strnow = now.strftime("%Y-%m-%d %H:%M:%S")

            msg = "#{0}\n您对{1}说：{2}\n".format(strnow, self.friend["user_name"], self.sendmsg_tc.GetValue())
            self.msglog += msg

            self.seemesg_tx.SetValue(self.msglog)

            # 光标显示在最后一行
            self.seemesg_tx.SetInsertionPointEnd()

            # 向服务器发送消息
            json_obj = {}
            json_obj["command"] = COMMAND_SENDMSG
            json_obj["user_id"] = self.user["user_id"]
            json_obj["message"] = self.sendmsg_tc.GetValue()
            json_obj["receive_user_id"] = self.friend["user_id"]

            # json 编码
            json_str = json.dumps(json_obj)
            client_socket.sendto(json_str.encode(), server_address)

            self.sendmsg_tc.SetValue("")

    def OnClose(self, event):
        # 停止线程
        self.isrunning = False
        self.t1.join()
        self.Hide()

        # 重启好友列表窗口的子线程
        self.friendsframe.reset_thread()
