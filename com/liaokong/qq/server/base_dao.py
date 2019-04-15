# -*- coding: utf-8 -*-
# Time    : 2019/4/14 12:29
# Author  : LiaoKong

"""定义DAO基类"""

import pymysql
import configparser
import logging

logger = logging.getLogger(__name__)


class BaseDao(object):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini", encoding="utf-8")

        host = self.config["db"]["host"]
        port = self.config.getint("db", "port")
        user = self.config["db"]["user"]
        password = self.config["db"]["password"]
        database = self.config["db"]["database"]
        charset = self.config["db"]["charset"]

        self.conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database,
                                    charset=charset)

    def close(self):
        """关闭数据库连接"""

        self.conn.close()
