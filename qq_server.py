# -*- coding: utf-8 -*-
# Time    : 2019/4/15 20:44
# Author  : LiaoKong

import logging
import socket
import sys
import traceback as tb
import json

from com.liaokong.qq.server.user_dao import UserDao

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(threadName)s "
                                               "- %(name)s - %(funcName)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

# 服务器
SERVER_IP = "127.0.0.1"
SERVER_PORT = 8888

# 操作命令代码
COMMAND_LOGIN = 1  # 登录命令
COMMAND_LOGOUT = 2  # 下线命令
COMMAND_SENDMSG = 3  # 发消息命令
COMMAND_REFRESH = 4  # 刷新好友列表命令

# 所有已经登录的客户端信息
client_list = []

# 初始化UDP Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))

logger.info("服务器启动，监听自己的端口{0}...".format(SERVER_PORT))

# 创建字节序列列表，作为接收数据的缓冲区
buffer = []

# 主循环
while 1:
    try:
        # 接收数据报包
        data, client_address = server_socket.recvfrom(1024)
        json_obj = json.loads(data.decode())

        logger.info("服务器端接收客户端的消息：{0}".format(json_obj))

        # 取出客户端传递过来的操作命令
        command = json_obj["command"]

        # 处理用户登录请求
        if command == COMMAND_LOGIN:
            userid = json_obj["user_id"]
            userpwd = json_obj["user_pwd"]

            logger.debug("user_id:{0} user_pwd:{1}".format(userid, userpwd))

            dao = UserDao()
            user = dao.find_by_id(userid)
            logger.info(user)

            # 判断客户端发送过来的密码是否与数据库一致
            if user is not None and user["user_pwd"] == userpwd:
                # 登录成功
                logger.info("登录成功")

                # 创建一个元组保存用户登录信息
                client_info = (userid, client_address)
                client_list.append(client_info)

                # 给客户端准备数据
                json_obj = user
                json_obj["result"] = "0"

                # 取出用户的好友列表
                dao = UserDao()
                friends = dao.find_friends(userid)

                # 返回在线好友id
                cinfo_userids = map(lambda it: it[0], client_list)

                for friend in friends:
                    fid = friend["user_id"]
                    # 添加好友状态 “1”为在线 “0”为离线
                    friend["online"] = "0"
                    if fid in cinfo_userids:
                        friend["online"] = "1"

                json_obj["friends"] = friends
                logger.info("服务器发送用户登录成功，消息{0}".format(json_obj))

            else:
                # 登录失败
                json_obj = {}
                json_obj["result"] = "-1"

            # JSON解码
            json_str = json.dumps(json_obj)

            # 给客户端发送数据
            server_socket.sendto(json_str.encode(), client_address)

        # 发送聊天消息
        elif command == COMMAND_SENDMSG:
            # 获得好友id
            fduserid = json_obj["receive_user_id"]
            # 向客户端发送数据
            # 在client_list中查找好友id
            filter_client_info = filter(lambda it: it[0] == fduserid, client_list)
            client_info = list(filter_client_info)

            if len(client_info) == 1:
                _, client_address = client_info[0]

                json_str = json.dumps(json_obj)
                server_socket.sendto(json_str.encode(), client_address)

        # 用户下线
        elif command == COMMAND_LOGOUT:
            userid = json_obj["user_id"]

            for client_info in client_list:
                cuerid, _ = client_info

                if cuerid == userid:
                    client_list.remove(client_info)
                    break

            logger.info(userid)

        # 刷新好友列表
        # 如果client_list中没有数据，调到下一个循环
        if not len(client_list):
            continue

        json_obj = {}
        json_obj["command"] = COMMAND_REFRESH
        # 返回在线好友id
        userids_map = map(lambda it: it[0], client_list)
        userid_list = list(userids_map)

        json_obj["OnlineUserList"] = userid_list

        for client_info in client_list:
            _, address = client_info

            # json解码
            json_str = json.dumps(json_obj)
            # 给客户端发送数据
            server_socket.sendto(json_str.encode(), address)

    except Exception:
        tb.print_exc()
        logger.info("超时")
