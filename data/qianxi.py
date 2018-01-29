#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
# import china
# from  city import CityObj

from  collections import  OrderedDict

from urllib import request, parse,error


class ChinaObj():
    def __init__(self):
        self.data= {
            'name': '全国',
            'type': 'map',
            'roam': 'true',
            'hoverable': 'false',
            'mapType': 'china',
            'itemStyle':{
                'normal':{
                    'borderColor':'rgba(100,149,237,1)',
                    'borderWidth':0.5,
                    'areaStyle':{
                        'color': '#1b1b1b'
                    }
                }
            },
            'data':[],
            'markLine' : {
                'smooth':'true',
                'symbol': ['none', 'circle'],
                'symbolSize' : 1,
                'itemStyle' : {
                    'normal': {
                        'color':'#fff',
                        'borderWidth':1,
                        'borderColor':'rgba(30,144,255,0.5)'
                    }
                },
                'data' : [
                    [{'name':'北京'},{'name':'包头'}],
                ],
            },
            'geoCoord': {
                '上海': [121.4648,31.2891],
                '东莞': [113.8953,22.901],
                '东营': [118.7073,37.5513],
                '中山': [113.4229,22.478],
                '临汾': [111.4783,36.1615],
                '临沂': [118.3118,35.2936],
                '丹东': [124.541,40.4242],
                '丽水': [119.5642,28.1854],
                '乌鲁木齐': [87.9236,43.5883],
                '佛山': [112.8955,23.1097],
                '保定': [115.0488,39.0948],
                '兰州': [103.5901,36.3043],
                '包头': [110.3467,41.4899],
                '北京': [116.4551,40.2539],
                '北海': [109.314,21.6211],
                '南京': [118.8062,31.9208],
                '南宁': [108.479,23.1152],
                '南昌': [116.0046,28.6633],
                '南通': [121.1023,32.1625],
                '厦门': [118.1689,24.6478],
                '台州': [121.1353,28.6688],
                '合肥': [117.29,32.0581],
                '呼和浩特': [111.4124,40.4901],
                '咸阳': [108.4131,34.8706],
                '哈尔滨': [127.9688,45.368],
                '唐山': [118.4766,39.6826],
                '嘉兴': [120.9155,30.6354],
                '大同': [113.7854,39.8035],
                '大连': [122.2229,39.4409],
                '天津': [117.4219,39.4189],
                '太原': [112.3352,37.9413],
                '威海': [121.9482,37.1393],
                '宁波': [121.5967,29.6466],
                '宝鸡': [107.1826,34.3433],
                '宿迁': [118.5535,33.7775],
                '常州': [119.4543,31.5582],
                '广州': [113.5107,23.2196],
                '廊坊': [116.521,39.0509],
                '延安': [109.1052,36.4252],
                '张家口': [115.1477,40.8527],
                '徐州': [117.5208,34.3268],
                '德州': [116.6858,37.2107],
                '惠州': [114.6204,23.1647],
                '成都': [103.9526,30.7617],
                '扬州': [119.4653,32.8162],
                '承德': [117.5757,41.4075],
                '拉萨': [91.1865,30.1465],
                '无锡': [120.3442,31.5527],
                '日照': [119.2786,35.5023],
                '昆明': [102.9199,25.4663],
                '杭州': [119.5313,29.8773],
                '枣庄': [117.323,34.8926],
                '柳州': [109.3799,24.9774],
                '株洲': [113.5327,27.0319],
                '武汉': [114.3896,30.6628],
                '汕头': [117.1692,23.3405],
                '江门': [112.6318,22.1484],
                '沈阳': [123.1238,42.1216],
                '沧州': [116.8286,38.2104],
                '河源': [114.917,23.9722],
                '泉州': [118.3228,25.1147],
                '泰安': [117.0264,36.0516],
                '泰州': [120.0586,32.5525],
                '济南': [117.1582,36.8701],
                '济宁': [116.8286,35.3375],
                '海口': [110.3893,19.8516],
                '淄博': [118.0371,36.6064],
                '淮安': [118.927,33.4039],
                '深圳': [114.5435,22.5439],
                '清远': [112.9175,24.3292],
                '温州': [120.498,27.8119],
                '渭南': [109.7864,35.0299],
                '湖州': [119.8608,30.7782],
                '湘潭': [112.5439,27.7075],
                '滨州': [117.8174,37.4963],
                '潍坊': [119.0918,36.524],
                '烟台': [120.7397,37.5128],
                '玉溪': [101.9312,23.8898],
                '珠海': [113.7305,22.1155],
                '盐城': [120.2234,33.5577],
                '盘锦': [121.9482,41.0449],
                '石家庄': [114.4995,38.1006],
                '福州': [119.4543,25.9222],
                '秦皇岛': [119.2126,40.0232],
                '绍兴': [120.564,29.7565],
                '聊城': [115.9167,36.4032],
                '肇庆': [112.1265,23.5822],
                '舟山': [122.2559,30.2234],
                '苏州': [120.6519,31.3989],
                '莱芜': [117.6526,36.2714],
                '菏泽': [115.6201,35.2057],
                '营口': [122.4316,40.4297],
                '葫芦岛': [120.1575,40.578],
                '衡水': [115.8838,37.7161],
                '衢州': [118.6853,28.8666],
                '西宁': [101.4038,36.8207],
                '西安': [109.1162,34.2004],
                '贵阳': [106.6992,26.7682],
                '连云港': [119.1248,34.552],
                '邢台': [114.8071,37.2821],
                '邯郸': [114.4775,36.535],
                '郑州': [113.4668,34.6234],
                '鄂尔多斯': [108.9734,39.2487],
                '重庆': [107.7539,30.1904],
                '金华': [120.0037,29.1028],
                '铜川': [109.0393,35.1947],
                '银川': [106.3586,38.1775],
                '镇江': [119.4763,31.9702],
                '长春': [125.8154,44.2584],
                '长沙': [113.0823,28.2568],
                '长治': [112.8625,36.4746],
                '阳泉': [113.4778,38.0951],
                '青岛': [120.4651,36.3373],
                '韶关': [113.7964,24.7028]
            }
        }

    def add_line(self,src='',tgt=''):
        line=[{'name': src[0]}, {'name': tgt[0]}]
        self.data['markLine']['data'].append(line)

    def add_geo(self,cityname,geo):
        print(cityname,geo)
        self.data[ 'geoCoord'][cityname]=[geo[0],geo[1]]





class CityObj(object):
    def __init__(self,cityname=''):
        self.data={
            'name': cityname,
            'type': 'map',
            'mapType': 'china',
            'data':[],
            'markLine' : {
                'smooth':'true',
                'effect' : {
                    'show': 'true',
                    'scaleSize': 1,
                    'period': 30,
                    'color': '#fff',
                    'shadowBlur': 10
                },
                'itemStyle' : {
                    'normal': {
                        'borderWidth':1,
                        'lineStyle': {
                            'type': 'solid',
                            'shadowBlur': 10
                        }
                    }
                },
                'data' : [
                ]
            },
            'markPoint' : {
                'symbol':'emptyCircle',
                'symbolSize' : 'function (v){return 10 + v/10}',
                'effect' : {
                    'show': 'true',
                    'shadowBlur' : 0
                },
                'itemStyle':{
                    'normal':{
                        'label':{'show':'false'}
                    },
                    'emphasis': {
                        'label':{'position':'top'}
                    }
                },
                'data' : [
                ]
            }
        }

    def add_line(self,src,tgt):
        # [{'name':'北京'}, {'name':'上海','value':95}],
        line=[{'name': src[0]}, {'name': tgt[0],'value':tgt[1]}]
        self.data['markLine']['data'].append(line)
        #{'name':'上海','value':95},
        line={'name': tgt[0],'value':tgt[1]}
        self.data['markPoint']['data'].append(line)


class OptionObj(object):
    def __init__(self):
        self.china = ChinaObj()
        with open('geos.txt' ,'rb') as rf:
            for line in rf:
                line=to_str(line).strip()
                if not line:
                    continue
                print(line)
                arr=line.split('\t')
                if len(arr) != 2:
                    continue
                c=arr[0]
                g=arr[1]
                arr=g.split(',')
                if len(arr) !=2:
                    continue
                geo=[ float(arr[0]),float( arr[1])]
                self.china.add_geo(c,geo)

        self.citymap={}
        self.data={
            'backgroundColor': '#1b1b1b',
            'color': ['gold', 'aqua', 'lime'],
            'title': {
                'text': '模拟迁徙',
                'subtext': '数据纯属虚构',
                'x': 'center',
                'textStyle': {
                    'color': '#fff'
                }
            },
            'tooltip': {
                'trigger': 'item',
                'formatter': '{b}'
            },
            'legend': {
                'orient': 'vertical',
                'x': 'left',
                'data': ['北京', '上海', '广州'],
                'selectedMode': 'single',
                'selected': {
                    '上海': 'false',
                    '广州': 'false'
                },
                'textStyle': {
                    'color': '#fff'
                }
            },
            'toolbox': {
                'show': 'true',
                'orient': 'vertical',
                'x': 'right',
                'y': 'center',
                'feature': {
                    'mark': {'show': 'true'},
                    'dataView': {'show': 'true', 'readOnly': 'false'},
                    'restore': {'show': 'true'},
                    'saveAsImage': {'show': 'true'}
                }
            },
            'dataRange': {
                'min': 0,
                'max': 100,
                'calculable': 'true',
                'color': ['#ff3333', 'orange', 'yellow', 'lime', 'aqua'],
                'textStyle': {
                    'color': '#fff'
                }
            }
        }

    '''
    src=[cityname,value,geo]
    '''
    def add_line(self,src,tgt):
        self.china.add_line(src,tgt)
        cityname=src[0]
        if cityname not in self.citymap:
            self.citymap[cityname]=CityObj(cityname)
        self.citymap[cityname].add_line(src,tgt)

    def build(self):
        self.data["series"]=[]
        self.data["series"].append(self.china.data)
        for item in self.citymap.values():
            self.data["series"].append( item.data)
        s = json.dumps(self.data, indent=2, ensure_ascii=False)
        data3='option = {0};'.format(s)
        print(data3)
        with open("result.txt",'wb') as wf:
            wf.write( to_bytes( data3) )


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



def address2geo(address):
    url="http://restapi.amap.com/v3/place/text"
    headers = {'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
              'Referer': r'http://lbs.amap.com/console/show/picker',
               'Connection': 'keep-alive'}
    data = {"s": "rsv3",
            "children": "",
            "key": "8325164e247e15eea68b59e89200988b",
            "page": 1,
            "offset": 10,
            "city": 310000,
            "language": "zh_cn",
            "callback": "jsonp_335848_",
            "platform": "JS",
            "logversion": "2.0",
            "sdkversion": 1.3,
            "appname": "http://lbs.amap.com/console/show/picker",
            "csid": "6B957AC3-0DC9-4795-B24B-D5AF07AE195D",
            "keywords": address}
    data = parse.urlencode(data).encode('utf-8')
    req = request.Request(url, headers=headers)
    try:
        page = request.urlopen(req, data=data).read()
        page = page.decode('utf-8')
        # print(page)
        p1=page.find("location")
        if p1<0:
            return ""
        p2=page.find('",',p1)
        if p2<0:
            return ""
        return page[p1+len('location":"'):p2]

    except error.HTTPError as e:
        print(e.code())
        print(e.read().decode('utf-8'))
    return ""

def pathsmake():
    import pandas as pd
    fn=r'D:\fs\h\d\diqu.csv'
    header = ['id','name','pid','py','level','city_code']
    df_city =  pd.read_csv(fn, sep=',', names=header,header=None)
    item = df_city[df_city['id'] == '530']



    def get_cityname(idx=''):
        item = df_city[df_city['id'] == str(idx)]
        if item['name'].values:
            return item['name'].values[0]
        return ""



    fn=r'D:\fs\h\d\chezhu.csv'
    header=['start_city',	'end_city']
    df_chezhu = pd.read_csv(fn, sep='\t', names=header, header=None)
    cnt=0
    paths={}
    for item in df_chezhu.values:
        if cnt==0:
            cnt +=1
            continue
        srcid,tgtid=item[0],item[1]
        if srcid not in paths:
            paths[srcid]={}
            paths[srcid][tgtid]=1
        elif tgtid not in  paths[srcid]:
            paths[srcid][tgtid] = 1
        else:
            paths[srcid][tgtid] +=1

    lines=[]
    wf=open('paths2.txt','wb')
    for srcid,vals in paths.items():
        # print(src,vals)
        src = get_cityname(srcid)
        if not src :
            print("cannot find srcid:"+srcid)
            sys.exit(0)
        for tgtid,va in vals.items():
            tgt = get_cityname(tgtid)
            if not tgt:
                print("cannot find tgt:" + tgtid)
                sys.exit(0)
            line=[src,tgt,va]
            print(line)
            wf.write( to_bytes(  str(line) ) )
            wf.write( to_bytes( '\n'))
    wf.close()

def geomake():
    import time
    cityname_set=set()
    with open('paths2.txt', 'rb') as rf:
        for line in rf:
                line=to_str(line).strip()
                if not line:
                    continue
                line=eval(line)
                print(line)
                cityname_set.add( line[0])
                cityname_set.add( line[1])
    with open('geos.txt','wb') as wf:
        for cityname in cityname_set:
            c=cityname+"市"
            geo = address2geo(c)
            line='{0}\t{1}'.format(cityname,geo)
            print(line)
            wf.write( to_bytes( line+"\n"))
            wf.flush()
            time.sleep(0.1)

def optmake():
    opt=OptionObj()
    with open('paths2.txt' ,'rb') as rf:
        for line in rf:
            line=to_str(line).strip()
            if not line:
                continue
            line=eval(line)
            if line[0] not in ['上海','北京' ]:
                continue
            print(line)
            opt.add_line(src=[line[0], 0], tgt=[line[1], line[2]])
    opt.build()


def main():
    # geomake()
    optmake()


    #



if __name__ == '__main__':
    main()


