# -*- coding: utf-8 -*-
# Time    : 2019/4/14 20:07
# Author  : LiaoKong


"""好友聊天窗口"""
import wx

from com.liaokong.qq.client.my_frame import MyFrame


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
        bottompanel.SetSizer(bottombox)

        self.sendmsg_tc = wx.TextCtrl(bottompanel)
        self.sendmsg_tc.SetFont(
            wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName="微软雅黑"))

        # 发送消息按钮
        sendmsg_btn = wx.Button(bottompanel, label="发送")
        self.Bind(wx.EVT_BUTTON, self.on_click, sendmsg_btn)

        bottombox.Add(self.sendmsg_tc, 5, wx.CENTER | wx.ALL | wx.EXPAND, border=5)
        bottombox.Add(sendmsg_btn, 1, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

        # 创建整体布局
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.seemesg_tx, 5, wx.CENTER | wx.ALL | wx.EXPAND, border=5)
        box.Add(bottombox, 1, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

        self.content_panel(box)

        # 消息日志
        self.msglog = ""

    def on_click(self, event):
        pass
