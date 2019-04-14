# -*- coding: utf-8 -*-
# Time    : 2019/4/14 20:46
# Author  : LiaoKong

import wx
import logging

from com.liaokong.qq.client.login_frame import LoginFrame

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(threadName)s "
                                               "- %(name)s - %(funcName)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)


class App(wx.App):
    def OnInit(self):
        # 创建登录窗口对象
        frame = LoginFrame()
        frame.Show()

        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()  # 进入主线程编程
