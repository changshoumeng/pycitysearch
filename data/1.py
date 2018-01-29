import heapq
import random


class TopkHeap(object):
    def __init__(self, k):
        self.k = k
        self.data = []

    def push(self, elem):
        if len(self.data) < self.k:
            heapq.heappush(self.data, elem)
        else:
            topk_big = self.data[0]
            if elem < topk_big:
                heapq.heapreplace(self.data, elem)

    def topK(self):
        return [x for x in reversed([heapq.heappop(self.data) for x in range(len(self.data))])]
        # return [heapq.heappop(self.data) for x in range(len(self.data))]


class TopkHeap2(object):
    def __init__(self, k):
        self.k = k
        self.data = []

    def push(self, elem):
        if len(self.data) < self.k:
            heapq.heappush(self.data, elem)
        else:
            topk_big = self.data[0]
            if elem < topk_big:
                heapq.heapreplace(self.data, elem)

    def topK(self):
        #return [x for x in reversed([heapq.heappop(self.data) for x in range(len(self.data))])]
        return [heapq.heappop(self.data) for x in range(len(self.data))]


if __name__ == "__main__":
    #list_rand = random.sample(range(1000000), 100)
    # list_rand=[11,2,2,33,4,5,6,77,8,8,334]
    # a = list(enumerate(list_rand))
    # print(a)
    # tp=TopkHeap(4)
    # print(heapq.nsmallest(4,a,key=lambda x:x[1]) )
    # for item in list_rand:
    #     tp.push(item)
    # print( tp.topK() )
    # print(    sorted(list_rand, reverse=False)[0:4] )
    a={}
    a[1]=20
    a[3]=2
    a[2]=40
    b=sorted( a.items(),key=lambda x:x[1])
    print(b)
