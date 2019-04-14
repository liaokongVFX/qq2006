# -*- coding: utf-8 -*-
# Time    : 2019/4/14 19:28
# Author  : LiaoKong
import wx
import wx.lib.scrolledpanel as scrolled

from com.liaokong.qq.client.my_frame import MyFrame


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

    def on_dclick(self, event):
        pass
