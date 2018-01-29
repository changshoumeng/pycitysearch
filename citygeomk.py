from math import radians, cos, sin, asin, sqrt
import pandas as pd
import time
import os
import json
import param


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

def get_province_dict():
    province=dict()
    fn=r'D:\fs\h\d\json\china.json'
    data=fileread(fn)
    js=json.loads(data)
    features= js["features"]
    for feature in features:
        #feature['id']
        properties=feature['properties']
        province[ properties["name"] ]= properties["cp"]
    return  province

def loadcg():
    cg=dict()
    with open(param.citygeo_fn, 'rb') as rf:
        for line in rf:
            line = to_str(line).strip()
            if not line:
                continue
            c=eval(line)
            cg[c[0]]=[c[1][0],c[1][1]]
    return cg


def savecg(cg={}):
    with open(param.citygeo_fn,'wb') as wf:
        for k,v in cg.items():
            item=(k,v)
            line=str(item)+"\n"
            wf.write( to_bytes( line))
    print("savecg ok;in {0}".format( param.citygeo_fn))




'''根据两点经纬度，计算两点的物理距离，单位是米'''
def haversine( src,tgt):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    lon1, lat1=src
    lon2, lat2=tgt

    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r * 1000

def fileread(fn):
    if not os.path.exists(fn):
        print("cannot find file:"+fn)
        return
    with open(fn,'rb') as rf:
        return to_str( rf.read( ))


def  loadcitylist():
    fn = r'data/diqu.csv'
    header = ['id', 'name', 'pid', 'py', 'level', 'city_code']
    df_city = pd.read_csv(fn, sep=',', names=header, header=None)

    city_id_map=dict()
    id_city_map=dict()
    cnt=0
    for item in df_city.values:
        if cnt == 0:
            cnt += 1
            continue
        # print(item)

        cityname = item[1]
        cid = item[0]
        id_city_map[cid]=cityname
        city_id_map[cityname]=cid
    return city_id_map,id_city_map

def dump_citygeoinfo():
    province_dic = get_province_dict()
    province_citylist_dict = dict()
    for province in province_dic.keys():
        province_citylist_dict[province] = []
        fn = r'D:\fs\h\d\json\{0}\{1}.json'.format(province, province)
        # print(fn)
        data = fileread(fn)
        js = json.loads(data)
        features = js["features"]
        for feature in features:
            # feature['id']
            properties = feature['properties']
            province_citylist_dict[province].append(properties)

    cg = dict()
    fn = r'D:\fs\h\d\diqu.csv'
    header = ['id', 'name', 'pid', 'py', 'level', 'city_code']
    df_city = pd.read_csv(fn, sep=',', names=header, header=None)

    def get_cityname(idx=''):
        item = df_city[df_city['id'] == str(idx)]
        if item['name'].values:
            return item['name'].values[0]
        return ""

    specials = ["377", "27", "419", "44"]
    zzq_pids = ["133", "309", "459", "322", "486"]
    tq_pids = ["467", "19", "436"]
    wrq_pids = ["328", "486", "459"]
    cnt = 0
    for item in df_city.values:
        if cnt == 0:
            cnt += 1
            continue
        # print(item)

        cityname = item[1]
        citylevel = item[4]
        pid = item[2]
        cid = item[0]

        if pid in specials:
            print("special item:{0}".format(item))
            continue

        if cid in specials:
            parentname = cityname
            cp = province_dic[parentname]
            cg[cityname] = cp
            continue

        if pid == '0':
            continue

        parentname = get_cityname(pid)
        if parentname not in province_citylist_dict:
            print("cannot find parentname:" + parentname)
            return

        isOK = False
        cp = []
        for properties in province_citylist_dict[parentname]:
            if cityname in properties["name"]:
                isOK = True
                cp = properties["cp"]
                break
        if not isOK:
            print("cannot find cityname:" + cityname)
            # print(province_citylist_dict[parentname])
            continue
        line = []
        for i in range(6):
            line.append(item[i])
        line.append(cp)
        print(line)
        cg[cityname] = cp
    savecg(cg)


def main():
    dump_citygeoinfo()

if __name__ == '__main__':
    main()
