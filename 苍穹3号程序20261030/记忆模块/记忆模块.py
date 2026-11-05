#记忆模块


#将当前的[senlist,actlist,vsum]加入自传体记忆memorylist中
def add_memorylist(senlist,actlist,vsum,memorylist):
    memorylist.append([senlist,actlist,vsum])
    return memorylist
