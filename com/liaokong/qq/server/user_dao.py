# -*- coding: utf-8 -*-
# Time    : 2019/4/14 12:40
# Author  : LiaoKong

"""用户管理DAO"""

from com.liaokong.qq.server.base_dao import BaseDao


class UserDao(BaseDao):
    def __init__(self):
        super(UserDao, self).__init__()

    def find_by_id(self, user_id):
        """根据用户id查询用户信息"""
        try:
            with self.conn.cursor() as cursor:
                sql = "select user_id,user_pwd,user_name,user_icon from users where user_id=%s"

                cursor.execute(sql, user_id)

                # 获取结果
                row = cursor.fetchone()
                if row is not None:
                    user = {}
                    user["user_id"] = row[0]
                    user["user_pwd"] = row[1]
                    user["user_name"] = row[2]
                    user["user_icon"] = row[3]

                    return user

        finally:
            self.close()

    def find_friends(self, user_id):
        """根据用户id查询用户信息"""

        users = []

        try:
            with self.conn.cursor() as cursor:
                sql = "select user_id,user_pwd,user_name,user_icon from users where " \
                      "user_id in (select user_id2 as user_id from friends where user_id1 = %s) or " \
                      "user_id in (select user_id1 as user_id from friends where user_id2 = %s)"

                cursor.execute(sql, (user_id, user_id))

                # 获取结果
                result_row = cursor.fetchall()
                for row in result_row:
                    user = {}
                    user["user_id"] = row[0]
                    user["user_pwd"] = row[1]
                    user["user_name"] = row[2]
                    user["user_icon"] = row[3]

                    users.append(user)

        finally:
            self.close()

        return users
