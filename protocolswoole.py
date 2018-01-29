#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import struct

# import stringutils
import stringutils


class COMMON(object):
    PACKET_HEAD_SIZE = 16
    MIN_PACKET_SIZE = 16
    MAX_PACKET_SIZE = 1024 * 1024 * 2  # Swoole协议报最大为2M
    PACKET_BODY_SIZE = MAX_PACKET_SIZE - MIN_PACKET_SIZE
    PACKET_TYPE_PHPSERIAL = 1
    PACKET_TYPE_JASONSERIAL = 2


class NET_PACKET(object):
    __slots__ = (
        "body_size", "packet_cmd", "packet_num", "service_index", "packet_type", "session_id", "transaction_id",
        "body",)

    def __init__(self):
        self.body_size = 0  # uint32
        self.packet_cmd = 0  # uint8
        self.packet_num = 0  # uint8
        self.service_index = 0  # uint8
        self.packet_type = 0  # uint8
        self.session_id = 0  # uint32
        self.transaction_id = 0  # uint32
        self.body = ""  # string

    def toStr(self):
        s = "size:{0} cmd:{1} num:{2} index:{3} type:{4} sesid:{5} transid:{6} body:{7}".format(self.body_size,
                                                                                                self.packet_cmd,
                                                                                                self.packet_num,
                                                                                                self.service_index,
                                                                                                self.packet_type,
                                                                                                self.session_id,
                                                                                                self.transaction_id,
                                                                                                self.body)
        return s

    def pack(self, packet_cmd=0, packet_num=0, service_index=0, packet_type=0, session_id=0, transaction_id=0, body=""):
        self.body_size = len(body)
        self.packet_cmd = packet_cmd
        self.packet_num = packet_num
        self.service_index = service_index
        self.packet_type = packet_type
        self.session_id = session_id
        self.transaction_id = transaction_id
        self.body = body
        formatStr = "!IBBBBII%ds" % (self.body_size)
        data = struct.pack(formatStr, self.body_size, self.packet_cmd, self.packet_num, self.service_index,
                           self.packet_type, self.session_id, self.transaction_id, stringutils.to_bytes(self.body))
        return data

    def packBody(self, body=""):
        self.body_size = len(body)
        self.body = body
        formatStr = "!IBBBBII%ds" % (self.body_size)
        data = struct.pack(formatStr, self.body_size, self.packet_cmd, self.packet_num, self.service_index,
                           self.packet_type, self.session_id, self.transaction_id, stringutils.to_bytes(self.body))
        return data

    '''data is bytearray,return field_list
    '''

    def unpack(self, data):
        if len(data) < 16:
            print("protocolswoole.unpack small:",len(data))
            return 0
        f1, f2, f3, f4, f5, f6, f7 = struct.unpack("!IBBBBII", data[0:16])
        self.body_size = f1
        self.packet_cmd = f2
        self.packet_num = f3
        self.service_index = f4
        self.packet_type = f5
        self.session_id = f6
        self.transaction_id = f7
        if self.body_size > COMMON.PACKET_BODY_SIZE:
            return -1
        if len(data) < self.body_size + 16:
            print("protocolswoole.unpack body_size not enough:", len(data),self.body_size)
            return 0
        self.body, = struct.unpack("!%ds" % self.body_size, data[16:16 + self.body_size])
        self.body = stringutils.to_str(self.body)
        return self.body_size + 16

    '''only unpack head
    '''

    def unpack_head(self, data):
        if len(data) < 16:
            return 0
        f1, f2, f3, f4, f5, f6, f7 = struct.unpack("!IBBBBII", data[0:16])
        self.body_size = f1
        self.packet_cmd = f2
        self.packet_num = f3
        self.service_index = f4
        self.packet_type = f5
        self.session_id = f6
        self.transaction_id = f7
        if self.body_size > COMMON.PACKET_BODY_SIZE:
            return -1
        if len(data) < self.body_size + 16:
            return 0
        return self.body_size + 16


def to_swoole_req(transid, call="", env="", params=[]):
    req = json.dumps({"call": call, "env": env, "params": params}, sort_keys=True, separators=(',', ':'))
    # print(req)
    json.loads(req)
    request_packet = NET_PACKET()
    return request_packet.pack(packet_cmd=0, packet_num=0, service_index=0, packet_type=COMMON.PACKET_TYPE_JASONSERIAL,
                               session_id=200, transaction_id=transid, body=req)


def to_swoole_rsp(code=0, data={}):
    rspobjobj = {}
    rspobjobj["errno"] = 0
    rspobjobj["data"] = {"code": code, "data": data}
    return json.dumps(rspobjobj, sort_keys=True, separators=(',', ':'))

if __name__ == '__main__':
    pass
