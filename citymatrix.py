import dijkstra
import citygeomk
import param
import numpy as np
import heapq
import math
import numpy as np
import time
import logging
logger = logging.getLogger()


def get_rotate_param(p,v):
    v=v*1.0/180*math.pi
    a, b,c=p
    param=[
        [math.cos(v),  -math.sin(v), -a*math.cos(v) + b*math.sin(v)+a],
        [math.sin(v),  math.cos(v), -a*math.sin(v) - b*math.cos(v)+b],
        [0,0,1]
    ]
    return param

def get_sexangle( p1,p2):
    plist = [p1,p2]
    p1=p1+[1]
    p2=p2+[1]
    px1=np.array(p1)
    px2=np.array(p2)
    cx=(px1+px2)/2
    px3 = np.dot( get_rotate_param(px1,60), cx)
    plist.append( px3.tolist()[:2])
    px4 = np.dot( get_rotate_param(px1,-60), cx)
    plist.append(px4.tolist()[:2])
    px5 = np.dot( get_rotate_param(px2,60), cx)
    plist.append(px5.tolist()[:2])
    px6 = np.dot( get_rotate_param(px2,-60), cx)
    plist.append(px6.tolist()[:2])
    # print(plist)
    return plist

def getCrossX(point,point1,point2):
    if point1[1] == point2[1]:
        return None
    if point[0] < min(point1[0], point2[0]):
        return None
    if point[0] > max(point1[0], point2[0]):
        return None
    x = (point[1]-point1[1]) * (point2[0]-point1[0])/(point2[1]-point1[1]) + point1[0]
    return x


def isPointinPolygon(point, rangelist):  #[[0,0],[1,1],[0,1],[0,0]] [1,0.8]
    # 判断是否在外包矩形内，如果不在，直接返回false
    lnglist = []
    latlist = []
    for i in range(  len(rangelist)  ):
        lnglist.append(rangelist[i][0])
        latlist.append(rangelist[i][1])
    # print(lnglist, latlist)
    maxlng = max(lnglist)
    minlng = min(lnglist)
    maxlat = max(latlist)
    minlat = min(latlist)
    # print(maxlng, minlng, maxlat, minlat)
    if (point[0] > maxlng or point[0] < minlng or
        point[1] > maxlat or point[1] < minlat):
        # print("很明显在边界外:{0}".format( point))
        return False
    return  True
    # count = 0
    # point1 = rangelist[0]
    # for i in range(1, len(rangelist)):
    #     point2 = rangelist[i]
    #     # 点与多边形顶点重合
    #     if ( point[0] == point1[0] and point[1] == point1[1]) or \
    #             (point[0] == point2[0] and point[1] == point2[1]):
    #         # print("在顶点上")
    #         return True
    #
    #     point12lng = getCrossX(point, point1, point2)
    #     # print(">>{0} --- {1}".format(point12lng,point[0] ) )
    #     if point12lng is not None:
    #         if (point12lng > point[0]):
    #             count +=1
    #
    #     point1 = point2

    # print(count)
    # if count%2 == 0:
    #     print("count%2 ")
    #     return False
    # else:
    #     return True

def isPointinValidArea(point,beginp,endp):
    sexangle=get_sexangle(beginp,endp)
    return isPointinPolygon(point,sexangle)

def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value  # Instance of bytes







class CityMatrix(object):
    def __init__(self):
        self.city_graph = dict()
        self.id_city_map = dict()
        self.city_id_map = dict()
        self.id_city_map2 = dict()
        self.city_id_map2 = dict()

        self.load()

    def get_geo(self,i):
        c=self.id_city_map[i]
        return self.city_graph[c]

    ''' 两个矢量是否在同一方向 '''
    def is_same_direction(self,a,b,c):
        ab=citygeomk.haversine(self.get_geo(a), self.get_geo(b))
        ac=citygeomk.haversine(self.get_geo(a), self.get_geo(c))
        bc=citygeomk.haversine(self.get_geo(b), self.get_geo(c))
        return ab**2+ac**2 > bc**2 +30000**2

    ''' 从b到c，假如经过a中转，是否太远了'''
    def is_long_direction(self,a,b,c):
        ab=citygeomk.haversine(self.get_geo(a), self.get_geo(b))
        ac=citygeomk.haversine(self.get_geo(a), self.get_geo(c))
        bc=citygeomk.haversine(self.get_geo(b), self.get_geo(c))
        return ab ** 2 + ac ** 2 > bc**2

    ''' 从b到c，计算出这量个点的可能要经历过的城市'''
    def get_cityidrange(self,cityid1,cityid2):
        geo1=self.get_geo( cityid1)
        geo2=self.get_geo( cityid2)
        sexangle = get_sexangle(geo1, geo2)
        cityid_validlist={cityid1}
        cityid_visitedlist={cityid1}
        #print(self.adjacency_mat[cityid1].items())
        def get_validcityids(cur_cityid):
            for k in self.adjacency_mat[cur_cityid]:
                # print("visit :" + self.id_city_map[k])
                if k  in cityid_visitedlist:
                    continue
                cityid_visitedlist.add(k)
                geo = self.get_geo(k)
                # print("will compute:{0}".format(geo))
                if isPointinPolygon( geo,sexangle):
                    if not self.is_long_direction(k,cityid1,cityid2):
                        cityid_validlist.add(k)
                        # print("in :" + self.id_city_map[k])
                    else:
                        #print("long :" + self.id_city_map[k])
                        pass
                else:
                    pass
                    # print("not in :"+ self.id_city_map[k])

                get_validcityids(k)

        get_validcityids(cityid1)
        if cityid2 not in cityid_validlist:
            logger.error("cityid2 not in,{0}>{1}is unreachable cityid2:{0}".format(cityid1,cityid2))
            return []
        return  cityid_validlist

    def create_smallworld(self, cityid1, cityid2,cityidrange):
        smallworld=dict()
        for cid in cityidrange:
            smallworld[cid] = { }
            for k, v in self.adjacency_mat[cid].items():
                if k in cityidrange:
                    if k == cid:
                        continue
                    smallworld[cid][k] = v
        return smallworld

    def distane(self,city1,city2):
        print(city1,city2)
        cityid1 = self.city_id_map[city1]
        cityid2 = self.city_id_map[city2]
        return  citygeomk.haversine(self.get_geo(cityid1), self.get_geo(cityid2))


    ''' 查询接口'''
    def query(self,city1="",city2="",scale=0):
        rsp = {}
        if city1 == city2:
            rsp["error"] = "src_city must be different with tgt_city"
            return rsp

        #兼容处理
        if city1.isdigit() :
            cityid1=city1
            cityid2=city2
            if cityid1 not in self.id_city_map2:
                rsp["error"] = "cannot find cityid:{0}".format(cityid1)
                return rsp
            if cityid2 not in self.id_city_map2:
                rsp["error"] = "cannot find cityid:{0}".format(cityid2)
                return rsp
            city1=self.id_city_map2[cityid1]
            city2=self.id_city_map2[cityid2]

        if city1 not in self.city_id_map:
            logger.debug("queryrequest c1x:{0} c2:{1} >canot find city ".format(city1, city2))
            rsp["error"] = "cannot find city:{0}".format(city1)
            return rsp

        if city2 not in self.city_id_map:
            logger.debug("queryrequest c1:{0} c2x:{1} >canot find city ".format(city1, city2))
            rsp["error"] = "cannot find city:{0}".format(city2)
            return rsp

        cityid1 = self.city_id_map[city1]
        cityid2 = self.city_id_map[city2]
        cityidrange = self.get_cityidrange(cityid1, cityid2)
        citynamerange = [self.id_city_map[x] for x in cityidrange]
        logger.debug("queryrequest,from {0} to {1}，cid:{2} > {3} range:{4}".format(city1, city2,cityid1,cityid2,citynamerange))

        neighbours=[]
        if scale > 0:
            ylist = self.distance_mat[cityid2]
            for i in range(  len(ylist) ):
                if ylist[i]<=scale * 1000:
                    neighbours.append( ( self.id_city_map[i] ,ylist[i]))

        neighbours=sorted(neighbours,key=lambda x:x[1])
        neighbours2=[  item[0]  for item in neighbours if item[0] != city2]

        if len(cityidrange) <=2:
            logger.debug("len(cityidrange) <=2: cityidrange:{0}".format(cityidrange) )
            rsp["from2"]=city1
            rsp["to2"]=city2
            rsp["distance"]=self.distane( city1,city2)
            rsp["pass2"]=[]
            rsp["pass"]=[ ]
            rsp["from"] = self.city_id_map2[city1]
            rsp["to"] = self.city_id_map2[city2]
            rsp["neighbours2"] = neighbours2
            rsp["neighbours"] = [self.city_id_map2[k] for k in neighbours2]
            return rsp

        smallworld =self.create_smallworld(cityid1, cityid2,cityidrange)
        # for k,v in smallworld.items():
        #     print(k,v)
        # print(">>>dijkstra...",len(smallworld))
        dis, paths = dijkstra.Dijkstra(smallworld, cityid1)
        # print(">>>dijkstra222...")

        result={}
        for k, plist in paths.items():
            c=self.id_city_map[k]
            result[c]={}
            result[c]["from2"]=city1
            result[c]["to2"]=city2
            result[c]["distance"]=dis[k]
            result[c]["pass2"]=[self.id_city_map[k] for k in plist]
            result[c]["pass"]=[ self.city_id_map2[ self.id_city_map[k] ] for k in plist]
            result[c]["from"] = self.city_id_map2[city1]
            result[c]["to"] = self.city_id_map2[city2]
            result[c]["neighbours2"]=neighbours2
            result[c]["neighbours"] = [ self.city_id_map2[k ] for k in neighbours2]

        if city2 not  in result:
            rsp["error"] = "city:{0},process error".format(city2)
            # print(result)
            return rsp

        rsp = result[city2]
        return rsp

    def queryallpath(self):
        citys = self.city_id_map.keys()
        with open("allpath.txt","wb") as wf:
            for c1 in citys:
                for c2 in citys:
                    if c1 != c2:
                        r = self.query(c1,c2)
                        ps=""
                        if "pass2" not in r:
                            ps=str(r)
                        else:
                            ps=r["pass2"]
                        line = "{0}\t{1}\t{2}\n".format(c1,c2,str(ps))
                        print(line)
                        to_bytes(line)
                        wf.write( to_bytes( line))






    def compute_distance_mat(self):
        length = len(self.city_graph)
        self.distance_mat = np.zeros((length, length))
        for x in range(length):
            self.distance_mat[x][x] = 0
            for y in range(x + 1, length):
                self.distance_mat[x][y] = citygeomk.haversine( self.get_geo(x), self.get_geo(y))
                self.distance_mat[y][x] = self.distance_mat[x][y]

    def compute_adjacency_mat(self):
        MIN_NEIGHBOURS_NUM= 6
        MAX_NEIGHBOURS_NUM= 16
        MAX_NEIGHBOURS_DISTANCE=200000
        length = len(self.city_graph)
        self.adjacency_mat = dict((k, dict()) for k in range(length))
        lines = []
        for x in range(length):
            ylist2 = list(enumerate(self.distance_mat[x]))
            topn = heapq.nsmallest(MAX_NEIGHBOURS_NUM, ylist2, key=lambda iter: iter[1])
            neighbours = []
            alist = []
            for elem in topn:
                if elem[1] == 0:
                    continue
                if len(neighbours) <= MIN_NEIGHBOURS_NUM:
                    neighbours.append(elem)
                    self.adjacency_mat[x][elem[0]] = elem[1]
                    desc = "{0}:{1}".format(self.id_city_map[elem[0]], elem[1])
                    alist.append(desc)
                    continue
                if elem[1] > MAX_NEIGHBOURS_DISTANCE:
                    break
                else:
                    neighbours.append(elem)
                    self.adjacency_mat[x][elem[0]] = elem[1]
                    desc = "{0}:{1}".format(self.id_city_map[elem[0]], elem[1])
                    alist.append(desc)

            line = "{0}\t{1}\n".format(self.id_city_map[x], ','.join(alist))
            lines.append(line)
        # print("loadok:"+param.neighbours_fn)
        with open(param.neighbours_fn, "wb") as wf:
            for line in lines:
                wf.write(to_bytes(line))
            for x in range(length):
                ydesc = str(self.adjacency_mat[x])
                wf.write(to_bytes(ydesc))
                wf.write(to_bytes("\n"))


    def load(self):
        self.city_id_map2,self.id_city_map2=citygeomk.loadcitylist()
        # print(self.city_id_map2)
        self.city_graph = citygeomk.loadcg()
        i = 0
        for c in self.city_graph.keys():
            self.id_city_map[i] = c
            self.city_id_map[c] = i
            i += 1
        self.compute_distance_mat()
        self.compute_adjacency_mat()

def main():
    cm=CityMatrix()
    city1, city2 = "上海", "南通"
    t1=time.time()

    p1=cm.query(city1,city2)

    print(p1)
    # cm.queryallpath()
    # dis1=cm.distane(city1,city2)
    # dis2=cm.distane(city2,city1)
    # print(dis1,dis2)

    # if r:
    #     print( r[city2])
    # else:
    #     print("seach failed")
    # print(time.time()-t1)


if __name__ == '__main__':
    import logging.config
    logging.config.fileConfig("conf/logging_debug.conf")
    main()
