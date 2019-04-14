# -*- coding: utf-8 -*-
# Time    : 2019/4/14 18:54
# Author  : LiaoKong

"""用户登录窗口"""

import json
import wx

from com.liaokong.qq.client.my_frame import MyFrame


class LoginFrame(MyFrame):
    def __init__(self):
        super(LoginFrame, self).__init__(title="QQ登录", size=(340, 255))

        # 窗口顶部图片
        topimage = wx.Bitmap("resources/images/QQll.JPG", wx.BITMAP_TYPE_JPEG)
        topimage_sb = wx.StaticBitmap(self.content_panel, bitmap=topimage)

        # 创建中间面板和控件
        middlepanel = wx.Panel(self.content_panel, style=wx.BORDER_DOUBLE)

        accountid_st = wx.StaticText(middlepanel, label="QQ号码")
        password_st = wx.StaticText(middlepanel, label="QQ密码")
        self.accountid_txt = wx.TextCtrl(middlepanel)
        self.password_txt = wx.TextCtrl(middlepanel, style=wx.TE_PASSWORD)

        st = wx.StaticText(middlepanel, label="忘记密码？")
        st.SetForegroundColour(wx.BLUE)

        # 创建FlexGrid布局
        fgs = wx.FlexGridSizer(3, 3, 8, 15)
        fgs.AddMany([(accountid_st, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.FIXED_MINSIZE),
                     (self.accountid_txt, 1, wx.CENTER | wx.EXPAND),
                     (wx.StaticText(middlepanel)),

                     (password_st, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.FIXED_MINSIZE),
                     (self.password_txt, 1, wx.CENTER | wx.EXPAND),
                     (st, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.FIXED_MINSIZE),

                     (wx.StaticText(middlepanel)),
                     (wx.CheckBox(middlepanel, -1, "自动登录"), 1, wx.CENTER | wx.EXPAND),
                     (wx.CheckBox(middlepanel, -1, "隐身登录"), 1, wx.CENTER | wx.EXPAND)
                     ])

        # 设置FlexGrid布局对象
        fgs.AddGrowableRow(0, 1)
        fgs.AddGrowableRow(1, 1)
        fgs.AddGrowableCol(0, 1)
        fgs.AddGrowableCol(1, 1)
        fgs.AddGrowableCol(2, 1)

        panelbox = wx.BoxSizer()
        panelbox.Add(fgs, -1, wx.CENTER | wx.ALL | wx.EXPAND, border=10)
        middlepanel.SetSizer(panelbox)

        # 创建按钮
        okb_btn = wx.Button(parent=self.content_panel, label="登录")
        self.Bind(wx.EVT_BUTTON, self.okb_btn_onclick, okb_btn)
        cancel_btn = wx.Button(parent=self.content_panel, label="取消")
        self.Bind(wx.EVT_BUTTON, self.cancel_btn_onclick, cancel_btn)

        # 创建水平Box布局
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.Button(parent=self.content_panel, label="申请号码"), 1, wx.CENTER | wx.ALL | wx.EXPAND, border=10)
        hbox.Add(okb_btn, 1, wx.CENTER | wx.ALL | wx.EXPAND, border=10)
        hbox.Add(cancel_btn, 1, wx.CENTER | wx.ALL | wx.EXPAND, border=10)

        # 创建垂直Box布局
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(topimage_sb, -1, wx.CENTER | wx.ALL, wx.EXPAND)
        vbox.Add(middlepanel, -1, wx.CENTER | wx.ALL, wx.EXPAND, border=5)
        vbox.Add(hbox, -1, wx.CENTER | wx.ALL, wx.EXPAND, border=1)

        self.content_panel.SetSizer(vbox)

    def okb_btn_onclick(self, event):
        pass

    def cancel_btn_onclick(self, event):
        pass
