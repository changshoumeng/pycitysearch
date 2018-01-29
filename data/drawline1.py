import random

import pylab
import math
import numpy as np

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


def isPointinPolygon(point, rangelist):  #[[0,0],[1,1],[0,1],[0,0]] [1,0.8]
    # 判断是否在外包矩形内，如果不在，直接返回false
    lnglist = []
    latlist = []
    for i in range(len(rangelist)-1):
        lnglist.append(rangelist[i][0])
        latlist.append(rangelist[i][1])
    # print(lnglist, latlist)
    maxlng = max(lnglist)
    minlng = min(lnglist)
    maxlat = max(latlist)
    minlat = min(latlist)
    print(maxlng, minlng, maxlat, minlat)
    if (point[0] > maxlng or point[0] < minlng or
        point[1] > maxlat or point[1] < minlat):
        return False
    count = 0
    point1 = rangelist[0]
    for i in range(1, len(rangelist)):
        point2 = rangelist[i]
        # 点与多边形顶点重合
        if (point[0] == point1[0] and point[1] == point1[1]) or (point[0] == point2[0] and point[1] == point2[1]):
            # print("在顶点上")
            return True
        # 判断线段两端点是否在射线两侧 不在肯定不相交 射线（-∞，lat）（lng,lat）
        if (point1[1] < point[1] and point2[1] >= point[1]) or (point1[1] >= point[1] and point2[1] < point[1]):
            # 求线段与射线交点 再和lat比较
            point12lng = point2[0] - (point2[1] - point[1]) * (point2[0] - point1[0])/(point2[1] - point1[1])
            print(point12lng)
            # 点在多边形边上
            if (point12lng == point[0]):
                # print("点在多边形边上")
                return True
            if (point12lng < point[0]):
                count +=1
        point1 = point2
    # print(count)
    if count%2 == 0:
        return False
    else:
        return True


class MiniPlotTool:
    '''
    A mini tool to draw lines using pylab
    '''
    basecolors = ['red', 'green', 'yellow', 'blue', 'black', 'cyan', 'magenta']

    def __init__(self, baseConfig):
        self.figsize = baseConfig.get('figsize', None)
        self.axis = baseConfig.get('axis', None)
        self.title = baseConfig.get('title', '')
        self.ylabel = baseConfig.get('ylabel', '')
        self.grid = baseConfig.get('grid', False)
        self.xaxis_locator = baseConfig.get('xaxis_locator', None)
        self.yaxis_locator = baseConfig.get('yaxis_locator', None)
        self.legend_loc = baseConfig.get('legend_loc', 0)
        if self.figsize != None:
            pylab.figure(figsize=self.figsize)
        if self.axis != None:
            pylab.axis(self.axis)
        pylab.title(self.title)
        pylab.ylabel(self.ylabel)
        ax = pylab.gca()
        pylab.grid(self.grid)
        if self.xaxis_locator != None:
            ax.xaxis.set_major_locator(pylab.MultipleLocator(self.xaxis_locator))
        if self.yaxis_locator != None:
            ax.yaxis.set_major_locator(pylab.MultipleLocator(self.yaxis_locator))
        self.lineList = []
        self.id = 1

    def addline(self, lineConf):
        self.lineList.append((self.id, lineConf))
        self.id += 1
        return {'id': self.id - 1}

    def removeline(self, lineId):
        for i in range(len(self.lineList)):
            id, conf = self.lineList[i]
            if id == lineId:
                del self.lineList[i]
                break
        else:
            return {'status': -1}
        # print len(self.lineList)
        return {'status': 0}

    def __parselineConf(self, lineConf):
        X = lineConf['X']
        Y = lineConf['Y']
        marker = lineConf.get('marker', None)
        color = lineConf.get('color', random.choice(MiniPlotTool.basecolors))
        markerfacecolor = lineConf.get('markerfacecolor', color)
        label = lineConf.get('label', '')
        linewidth = lineConf.get('linewidth', 1)
        linestyle = lineConf.get('linestyle', '-')
        return X, Y, marker, color, markerfacecolor, label, linewidth, linestyle

    def plotSingleLine(self, lineConf):
        X, Y, marker, color, markerfacecolor, label, linewidth, linestyle = self.__parselineConf(lineConf)
        pylab.plot(X, Y, marker=marker, color=color, markerfacecolor=markerfacecolor, label=label, linewidth=linewidth,
                   linestyle=linestyle)
        pylab.legend(loc=self.legend_loc)

    def plot(self):
        colors = [MiniPlotTool.basecolors[i % len(MiniPlotTool.basecolors)] for i in range(len(self.lineList))]
        for i in range(len(self.lineList)):
            id, conf = self.lineList[i]
            if conf.get('color', None):
                conf['color'] = colors[i]
            X, Y, marker, color, markerfacecolor, label, linewidth, linestyle = self.__parselineConf(conf)
            # pylab.plot(X,Y)
            pylab.plot(X, Y, marker=marker, color=color, markerfacecolor=markerfacecolor, label=label,
                       linewidth=linewidth, linestyle=linestyle)

        pylab.legend(loc=self.legend_loc)

    def show(self):
        pylab.show()


    def drawline(self,  pos1,pos2 ):
        X=[pos1[0],pos2[0]]
        Y=[pos1[1],pos2[1]]
        lineConf3 = {'X': X, 'Y': Y, 'marker': 'o', 'color': 'b', 'markerfacecolor': 'r', 'linewidth': 3,'linestyle': '-'}
        self.addline(lineConf3)

    def drawgraph(self):
        G = {1: {1: 0, 2: 1, 3: 12},
             2: {2: 0, 3: 9, 4: 3},
             3: {3: 0, 5: 5},
             4: {3: 4, 4: 0, 5: 13, 6: 15},
             5: {5: 0, 6: 4},
             6: {6: 0}
             }



def main():
    # test
    baseConfig = {
        'figsize' : (6,8),
        'axis': [0,20,0,20],
        'title' : 'hello title',
        'ylabel' : 'hello ylabel',
        'grid': True,
        'xaxis_locator' : 0.5,
        'yaxis_locator' : 1,
        'legend_loc' : 'upper right'
         }
    tool = MiniPlotTool(baseConfig)

    p1=[5,5]
    p2=[10,10]
    plist = get_sexangle(p1,p2)

    t=isPointinPolygon( [5.5,4.5], plist)
    print(t)

    X = []
    Y = []
    for p in plist:
        X.append( p[0])
        Y.append( p[1])


    lineConf = {'X': X,
                'Y': Y,
                'marker' : 'x',
                'color' : 'b',
                 'markerfacecolor' : 'r',
                'label' : '222',
                'linewidth' : 0.1,
                'linestyle' : '--'
                }

    # tool.plotSingleLine(lineConf)
    tool.addline(lineConf)
    # tool.addline(lineConf2)
    # tool.drawline( pos1=(1,1),pos2=(2,2))
    # print tool.removeline(1)

    tool.plot()
    tool.show()
    pass



if __name__ == '__main__':
    main()