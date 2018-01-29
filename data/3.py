import pandas as pd
import os
import json

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

def fileread(fn):
    if not os.path.exists(fn):
        print("cannot find file:"+fn)
        return
    with open(fn,'rb') as rf:
        return to_str( rf.read( ))

'''
		'name': '香港',
		'cp': [114.173355, 22.320048],
		'childNum': 5
'''
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

def main():
    province_dic=get_province_dict()
    province_citylist_dict=dict()
    for province in province_dic.keys():
        province_citylist_dict[province]=[]
        fn=r'D:\fs\h\d\json\{0}\{1}.json'.format(province,province)
        #print(fn)
        data=fileread(fn)
        js = json.loads(data)
        features = js["features"]
        for feature in features:
            # feature['id']
            properties = feature['properties']
            province_citylist_dict[province].append( properties)

    cg=dict()
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
    cnt=0
    for item in df_city.values:
        if cnt==0:
            cnt +=1
            continue
        #print(item)

        cityname=item[1]
        citylevel=item[4]
        pid=item[2]
        cid=item[0]

        if pid in specials :
            print("special item:{0}".format(item))
            continue

        if cid in specials:
            parentname = cityname
            cp=province_dic[parentname]
            cg[cityname] = cp
            continue

        if pid=='0' :
            continue

        parentname = get_cityname( pid )
        if parentname not in province_citylist_dict:
            print("cannot find parentname:"+parentname)
            return

        isOK=False
        cp=[]
        for properties in province_citylist_dict[parentname]:
            if cityname  in  properties["name"]:
                isOK=True
                cp=properties["cp"]
                break
        if not isOK:
            print("cannot find cityname:" + cityname)
            # print(province_citylist_dict[parentname])
            continue
        line=[]
        for i in range(6):
            line.append( item[i])
        line.append( cp)
        print(line)

        cg[cityname] = cp

    # for province, cp in province_dic.items():
    #     cg[province] = cp

    with open("citygeo.txt",'wb') as wf:
        for k,v in cg.items():
            item=(k,v)
            line=str(item)+"\n"
            wf.write( to_bytes( line))







if __name__ == '__main__':
    main()
    print("DONE")
