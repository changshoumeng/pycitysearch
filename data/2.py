import numpy as np
import math

def get_param(p,v):
    a, b,c=p
    param=[
        [math.cos(v),-math.sin(v),-a*math.cos(v)+b*math.sin(v)+a],
        [math.sin(v), math.cos(v), -a * math.sin(v) - b * math.cos(v) + b],
        [0,0,1]
    ]
    return param


def main():
    p1=[1,1,1]
    p2=[5,5,1]
    px1=np.array(p1)
    px2=np.array(p2)
    cx=(px1+px2)/2
    print(cx)
    plist=[]
    px3 = np.dot( get_param(px1,60), cx)
    plist.append( px3.tolist()[:2])
    px4 = np.dot( get_param(px1,-60), cx)
    plist.append(px4.tolist()[:2])
    px5 = np.dot( get_param(px2,60), cx)
    plist.append(px5.tolist()[:2])
    px6 = np.dot( get_param(px2,-60), cx)
    plist.append(px6.tolist()[:2])
    print(plist)



main()