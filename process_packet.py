#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################
#   A clever person solves a problem. A wise person avoids it
#   Please call Me programming devil.
#
#
######################################################## #
import json
import logging
import sys
import traceback
import  citymatrix
from pyxxnet3 import public_server_interface
import app_core_handler,protocolswoole


logger = logging.getLogger()

class GLOBAL:
    my_citymatrix = citymatrix.CityMatrix()

# @pram session
# @pram packet_cmd
# @pram packet_data
def session_dispatch_packet(session, packet_cmd, packet_data):
    # print("session_dispatch_packet():",packet_data)
    sessionid = session.get_session_uid()
    workercount = app_core_handler.APP_CORE_HANDLER.workerconfig_get("workercount")
    if workercount == 0:
        rsp = process_task(None, packet_cmd, packet_data)
        if rsp:
            public_server_interface.send_to_session(sessionid, rsp)
        return
    # transid = _my_trans_map.add(sessionid, packet)
    public_server_interface.send_to_taskQ(public_server_interface.MsgObject(sessionid, (packet_cmd, packet_data)))


def process_task(worker, packet_cmd, packet_data):
    packet = protocolswoole.NET_PACKET()
    ret=packet.unpack(packet_data)
    if ret <= 0:
        logger.error("process_task;packet.unpack(packet_data);failed;{0} {1} {2}".format("", ret,packet_data))
        return
    return task_onSearchPaths(worker,packet)

def task_onSearchPaths( worker, packet):
    # logger.debug("deeplearn_text_gettags;%s", packet.body)
    code=0
    data={}
    jsobj=None
    try:
        jsobj = json.loads(packet.body)
        call = jsobj["call"]
        params = jsobj["params"]
        # if 1==1 and call == "deepLearning\\text\\text::gettags":
        if 1 == 1:
            if len(params) < 3:
                code = 400
                data = {"error": "params invalid,len(params)<3"}
            else:
                code = 0
                src_city = params[0]
                tgt_city = params[1]
                scale = params[2]
                if not scale:
                    scale=0
                data=GLOBAL.my_citymatrix.query(src_city,tgt_city,int(scale) )
                code = 0 if "error" not  in data else 404
        else:
            logger.warning("invalid call:%s", call)
            code = 900
            data = {"error": "not support the call:" + call}
            pass
    except TypeError as  e:
        logger.critical("Catch TypeError:%s", repr(e))
        logger.critical("Error String is:%s", packet.body)
        code = 901
        data = {"error": "TypeError: please check names(call,params,env)"}
    except Exception as e:
        code = 1000
        data = {"error": "uncaught excepthion,server error {0} inlen:{1}".format(str(e), len(packet.body))}
        info = sys.exc_info()
        t = '**************caught exception*************'
        for f, l, func, text in traceback.extract_tb(info[2]):
            t += "\n[file]:{0} [{1}] [{2}] {3}".format(f, l, func, text)
        t += "\n[info]:%s->%s\n" % info[:2]
        logger.exception(t)
    pass
    # if code != 0:
    #     logger.error("process faild;{0}".format(str(data)))
    rsp = protocolswoole.to_swoole_rsp(code, data)
    logger.debug("request:{0}".format(jsobj))
    logger.debug("response:{0}".format(data))
    return packet.packBody(rsp)
    # public_server_interface.send_to_session(sessi