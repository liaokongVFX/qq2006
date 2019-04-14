# -*- coding: utf-8 -*-
# Time    : 2019/4/14 18:29
# Author  : LiaoKong

"""定义Frame窗口基类"""

import logging
import socket
import sys

import wx

logger = logging.getLogger(__name__)

# 服务器
SERVER_IP = "127.0.0.1"
SERVER_PORT = 8888

server_address = (SERVER_IP, SERVER_PORT)

# 操作命令代码
COMMAND_LOGIN = 1  # 登录命令
COMMAND_LOGOUT = 2  # 下线命令
COMMAND_SENDMSG = 3  # 发消息命令
COMMAND_REFRESH = 4  # 刷新好友列表命令

# 初始化UDP Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 设置socket超时一秒，不在等待接收数据
client_socket.settimeout(1)


class MyFrame(wx.Frame):
    def __init__(self, title, size):
        super(MyFrame, self).__init__(parent=None, title=title, size=size,
                                      style=wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX)

        # 设置窗口居中
        self.Center()

        # 设置Frame窗口内容面板
        self.content_panel = wx.Panel(parent=self)

        # 设置图标
        ico = wx.Icon("resources/icon/qq.ico")

        # 设置窗口最大和最小尺寸
        self.SetSizeHints(size, size)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, event):
        # 推出系统
        self.Destroy()
        client_socket.close()
        sys.exit()
