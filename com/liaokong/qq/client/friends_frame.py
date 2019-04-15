# -*- coding: utf-8 -*-
# Time    : 2019/4/14 19:28
# Author  : LiaoKong
import json
import threading

import wx
import wx.lib.scrolledpanel as scrolled

from com.liaokong.qq.client.chat_frame import ChatFrame
from com.liaokong.qq.client.my_frame import *


class FriendsFrame(MyFrame):
    def __init__(self, user):
        super(FriendsFrame, self).__init__(title="我的好友", size=(260, 600))

        self.chatFrame = None

        # 用户信息
        self.user = user

        # 好友列表
        self.friends = user["friends"]

        # 好友控件列表
        self.friend_controls = []

        user_icon_file = "resources/images/{0}.jpg".format(user["user_icon"])
        user_icon = wx.Bitmap(user_icon_file, wx.BITMAP_TYPE_JPEG)

        # 顶部面板
        toppanel = wx.Panel(self.content_panel)
        user_icon_sbitmap = wx.StaticBitmap(toppanel, bitmap=user_icon)
        username_st = wx.StaticText(toppanel, style=wx.ALIGN_CENTER_HORIZONTAL, label=user["user_name"])

        # 创建顶部布局
        topbox = wx.BoxSizer(wx.VERTICAL)
        topbox.AddSpacer(15)
        topbox.Add(user_icon_sbitmap, 1, wx.CENTER)
        topbox.AddSpacer(5)
        topbox.Add(username_st, 1, wx.CENTER)
        toppanel.SetSizer(topbox)

        # 好友列表面板
        panel = scrolled.ScrolledPanel(self.content_panel, -1, size=(206, 1000), style=wx.DOUBLE_BORDER)

        gridsizer = wx.GridSizer(cols=1, rows=20, gap=(1, 1))
        if len(self.friends) > 20:
            gridsizer = wx.GridSizer(cols=1, rows=len(self.friends), gap=(1, 1))

        # 添加好友到好友列表面板
        for index, friend in enumerate(self.friends):
            friend_panel = wx.Panel(panel, id=index)

            fdname_st = wx.StaticText(friend_panel, id=index, style=wx.ALIGN_CENTER_HORIZONTAL,
                                      label=friend["user_name"])

            fdqq_st = wx.StaticText(friend_panel, id=index, style=wx.ALIGN_CENTER_HORIZONTAL,
                                    label=friend["user_id"])

            path = "resources/images/{0}.jpg".format(friend["user_icon"])
            icon = wx.Bitmap(path, wx.BITMAP_TYPE_JPEG)

            if friend["online"] == "0":
                icon2 = icon.ConvertToDisabled()
                fdicon_sb = wx.StaticBitmap(friend_panel, id=index, bitmap=icon2, style=wx.BORDER_RAISED)
                fdicon_sb.Enable(False)
                fdname_st.Enable(False)
                fdqq_st.Enable(False)
                self.friend_controls.append((fdname_st, fdqq_st, fdicon_sb, icon))

            else:
                fdicon_sb = wx.StaticBitmap(friend_panel, id=index, bitmap=icon, style=wx.BORDER_RAISED)
                fdicon_sb.Enable(True)
                fdname_st.Enable(True)
                fdqq_st.Enable(True)
                self.friend_controls.append((fdname_st, fdqq_st, fdicon_sb, icon))

            # 为好友图标和昵称和qq控件添加双击事件
            fdicon_sb.Bind(wx.EVT_LEFT_DCLICK, self.on_dclick)
            fdname_st.Bind(wx.EVT_LEFT_DCLICK, self.on_dclick)
            fdqq_st.Bind(wx.EVT_LEFT_DCLICK, self.on_dclick)

            friendbox = wx.BoxSizer(wx.HORIZONTAL)
            friendbox.Add(fdicon_sb, 1, wx.CENTER)
            friendbox.Add(fdqq_st, 1, wx.CENTER)
            friendbox.Add(fdname_st, 1, wx.CENTER)

            friend_panel.SetSizer(friendbox)

            gridsizer.Add(friend_panel, 1, wx.ALL, border=5)

        panel.SetSizer(gridsizer)

        # 整体box布局
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(toppanel, -1, wx.CENTER | wx.EXPAND)
        box.Add(panel, -1, wx.CENTER | wx.EXPAND)

        self.content_panel.SetSizer(box)

        # 初始化线程
        # 设置子线程状态
        self.isrunning = True
        # 创建一个子线程
        self.t1 = threading.Thread(target=self.thread_body)
        self.t1.start()

    def on_dclick(self, event):
        # 获取选中好友列表索引
        fid = event.GetId()

        if self.chatFrame is not None and self.chatFrame.IsShown():
            dlg = wx.MessageDialog(self, "聊天窗口已经打开", "操作失败", wx.OK | wx.ICON_ERROR)

            dlg.ShowModal()
            dlg.Destroy()
            return

            # 停止当前窗口中的线程
        self.isrunning = False
        self.t1.join()

        self.chatFrame = ChatFrame(self, self.user, self.friends[fid])
        self.chatFrame.Show()

        event.Skip()

    def refresh_friend_list(self, online_user_list):
        for index, friend in enumerate(self.friends):
            friend_userid = friend["user_id"]
            fdname_st, fdqq_st, fdicon_sb, fdicon = self.friend_controls[index]

            if friend_userid in online_user_list:
                fdname_st.Enable(True)
                fdqq_st.Enable(True)
                fdicon_sb.Enable(True)
                fdicon_sb.SetBitmap(fdicon)

            else:
                fdname_st.Enable(False)
                fdqq_st.Enable(False)
                fdicon_sb.Enable(False)
                fdicon_sb.SetBitmap(fdicon.ConvertToDisabled())

        # 重绘窗口 显示更换后的图片
        self.content_panel.Layout()

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
                        self.refresh_friend_list(userid_list)

            except Exception:
                continue

    # 重启子线程
    def reset_thread(self):
        # 子线程运行状态
        self.isrunning = True
        # 创建一个子线程
        self.t1 = threading.Thread(target=self.thread_body)
        self.t1.start()

    def OnClose(self, event):
        if self.chatFrame is not None and self.chatFrame.IsShown():
            dlg = wx.MessageDialog(self, "请先关闭聊天窗口，再关闭好友列表窗口", "操作失败", wx.OK | wx.ICON_ERROR)

            dlg.ShowModal()
            dlg.Destroy()

            return

        # 当前用户下线 给服务器发送下线消息
        json_obj = {}
        json_obj["command"] = COMMAND_LOGOUT
        json_obj["user_id"] = self.user["user_id"]

        json_str = json.dumps(json_obj)
        client_socket.sendto(json_str.encode(), server_address)

        # 停止当前子线程
        self.isrunning = False
        self.t1.join()
        self.t1 = None

        # 关闭窗口
        super(FriendsFrame, self).OnClose(event)
