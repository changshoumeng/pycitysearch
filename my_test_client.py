#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:zhangtao
# pycitysearch 服务的测试客户端，包括了本服务的测试用例，用以说明如何实现RPC来使用本服务
import socket
import time
import json
import protocolswoole

'''全局参数管理器'''
class GLOBAL:
    host = ("127.0.0.1", 9415)
    # host =("183.57.37.220",10004)
#
def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value  # Instance of str


def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value  # Instance of bytes

'''
接口：实现网络IOCtrl，建立连接，发送一个请求，等待，直到收到响应，返回
'''
def net_ioctrl(address=(), request="", recvsize=8192*100):
    socket.setdefaulttimeout(30)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        t1 = time.time()
        client_socket.connect(address)
        t2 = time.time()-t1
        print("connectok,address:{0} usetime:{1}s".format(address,t2) )

        t1 = time.time()
        ret=client_socket.send(request)
        t2 = time.time() - t1
        print("sendok,sendret:{0} usetime:{1}".format( ret,t2) )

        t1 = time.time()
        rsp = client_socket.recv(recvsize)
        waitcnt=0
        while waitcnt<3:
            if len(rsp)>16:
                break
            data= client_socket.recv(recvsize)
            if not data:
                break
            rsp += data
            waitcnt +=1
        t2 = time.time() - t1
        print("recvok,recvret:{0} usetime:{1}".format(len(rsp),t2) )
        return rsp
    except socket.timeout:
        t = "net_ioctrl timeout> addr:{0}".format(address)
        print(t)
    except Exception as e:
        t = "net_ioctrl exception> addr:{0} {1}".format(address, repr(e))
        print(t)
    finally:
        client_socket.close()



'''
接口描述：查询两点之间的捷径的路线
输入：city1 起始点
      city2 终止点
输出：
'data': {
	'distance': 853487.7838739048,
	'to': '武汉',
	'from': '上海',
	'pass': ['无锡', '常州', '镇江', '马鞍山', '芜湖', '铜陵', '安庆', '九江', '黄石']
}   
'''
def query_citypaths(city1,city2,scale=100):
    call = "DeepLearning\search\search::citypaths"
    req = protocolswoole.to_swoole_req(transid=0, call=call, env="", params=[city1, city2,scale])
    rsp = net_ioctrl(GLOBAL.host, req)
    print("--------rsp--------")
    if not rsp:
        print("net_ioctrl failed>")
        return
    # print(rsp)
    packet = protocolswoole.NET_PACKET()
    packet.unpack(rsp)
    print(packet.body)
    print("--------to json------------")
    print(json.loads(packet.body) )

def t_query_citypaths():
    city1="广州"
    city2="武汉"
    t1=time.time()
    #{'call': 'DeepLearning\\search\\search::citypaths', 'params': ['92', '170', '']}

    # query_citypaths('92', '170',100)
    query_citypaths(city1,city2)
    t2=time.time()-t1
    print("finish query_citypaths,usetime:{0}s".format( t2))


def main():
    t_query_citypaths()


if __name__ == '__main__':
    main()

