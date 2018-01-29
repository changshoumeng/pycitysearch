这是一个什么服务?
计算一个地图上两个城市之间的最短路径。
citymatrix.py 是核心模块，采用的搜索算法dijkstra.py

输入：  出发城市，终点城市
输出：  从出发点到终点，要途径的最短城市序列
        终点城市的方圆100公里的城市序列

如何启动？

#!/bin/bash
set -x
NOWDIR=`pwd`
rm -rf log/*
rm -rf run/*
nohup python  pycitysearch.py  > $NOWDIR/log/unhandle_error.log 2>&1 &

如何停止？

 python  pycitysearch.py  stop