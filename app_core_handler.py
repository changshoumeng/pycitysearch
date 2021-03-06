#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################
#   A clever person solves a problem. A wise person avoids it
#   Please call Me programming devil.
#
#
#
#
#
######################################################## #
import logging
logger = logging.getLogger()

from pyxxnet3 import public_server_callback
from pyxxnet3 import public_server_interface
import process_packet,app_worker,param,protocolswoole



class APP_CORE_HANDLER(public_server_callback.ServerCallback):
    endpoint_ids = [i for i in range(1)]
    endpoint_session_map = {}
    session_endpoint_map = {}
    worker = app_worker.AppWorker()
    python = "python"

    def __init__(self):
        pass

    @staticmethod
    def my_servername():
        return param.service_name

    '''本服务 启用此接口'''
    @staticmethod
    def listenconfig_get(key=""):  # 10.10.2.143
        c = {"addresslist": [("0.0.0.0", 9415, 0)], "eventloop": "select", }
        return c[key]

    '''本服务 禁用此接口'''
    @staticmethod
    def connectconfig_get(key=""):
        server_addr_list = [("127.0.0.1", 9414, i) for i in APP_CORE_HANDLER.endpoint_ids]
        c = {"addresslist": server_addr_list, "eventloop": "select", }
        return ""

    '''本服务 禁用此接口'''
    @staticmethod
    def workerconfig_get(key=""):
        c = {"workercount": 0, }
        return c[key]

    '''本服务 启用此接口'''
    # @return: len(buffer),0  <size,cmd>
    @staticmethod
    def session_unpack_frombuffer(session, buffer):
        net_head = protocolswoole.NET_PACKET()
        ret = net_head.unpack_head(buffer)
        if ret < 0:
            logger.error("session_unpack_frombuffer failed; buffer:{0}".format( buffer))
            return (-1, 0)
        if ret == 0:
            # print("wait for more bytes")
            logger.debug("wait for more bytes ; bufferlen:{0}".format( len(buffer) ) )
            return (0, 0)
        return (16 + net_head.body_size, net_head.packet_cmd)

    '''本服务 启用此接口'''
    # session_dispatch_packet
    # this method ,call in main thread; and decide woker who will process the packet
    # @param  session.get_sessino_uid()
    # @note: process_packet is user defined module
    @staticmethod
    def session_dispatch_packet(session, packet_cmd, packet_data):
        # print("session_dispatch_packet:", session, packet_cmd,packet_data)
        # if packet_cmd == 0:
        #     session.send(packet_data)
        #     return
        process_packet.session_dispatch_packet(session, packet_cmd, packet_data)

    '''本服务 禁用此接口'''
    @staticmethod
    def task_on_rsp(session_uid, session_data):
        cmd, packet_data = session_data
        logger.debug("task_on_rsp: %s cmd:%d size:%d", str(session_uid), cmd, len(packet_data))
        public_server_interface.send_to_session(session_uid, packet_data)
