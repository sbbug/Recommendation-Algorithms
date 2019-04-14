# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 21:19:04 2019

@author: sun
"""
import pandas as pd
import numpy as np

#计算余弦相似度
def cosSim(vector_a, vector_b):
    """
    计算两个向量之间的余弦相似度
    :param vector_a: 向量 a
    :param vector_b: 向量 b
    :return: sim
    """
    vector_a = np.mat(vector_a)
    vector_b = np.mat(vector_b)
    num = float(vector_a * vector_b.T)
    denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    cos = num / denom
    sim = 0.5 + 0.5 * cos
    return sim

# 加载数据，并做预处理
def loadData(file_path,cols):

    # 读取数据
    data = pd.read_excel(file_path,names=cols)#

    # 数据预处理，删除含有NAN的行
    data = data.dropna(axis=0,how='any')

    # 删除指定列,删除单价与总价
    data = data.drop('price', 1)
    data = data.drop('cash', 1)

    return data


# 获取user_item矩阵
def getUserItem(user_count, item_count, users, items):

    # 开始算法部分
    # 定义user_item(u,i),表示用户u对物品i的喜好程度，用户*商品矩阵，值存储的值是rating
    user_item = np.zeros((user_count, item_count))

    # 生成user_item矩阵
    for u in range(len(users)):
        # if i==1: break
        temp = data[data['user_id'] == users[u]]
        for index, row in temp.iterrows():
            # 根据商品名字获取商品下标
            k = items.index(row['item'])
            # print(u,k)
            user_item[u][k] = row['count']
            # print(row)
        # R[][]
        # i=i+1
    return user_item

# 获取item_item的矩阵
def getItemItem(item_count,user_item):
    # 计算基于item的相似度，使用余弦相似度计算
    item_item = np.zeros((item_count, item_count))

    for i in range(item_count):
        for j in range(item_count):
            item_item[i][j] = cosSim(user_item[:, i], user_item[:, j])  # 计算余弦相似度

    return item_item

#获取一个向量里所有不为零的下标,获取用户喜欢物品集合下标
def getUserLike(vec):
    items = []
    for i in range(len(vec)):
        if vec[i]!=0:
            items.append(i)

    return items

#对item_item里，获取与物品j最相似的k个商品
def getSimilarKItem(vec,k):

    vec_temp = vec.copy()
    vec = sorted(vec)
    vec_index = []
    res = vec[:k]

    for i in range(len(res)):
        index = np.argwhere(vec_temp==res[i])
        vec_index.append(index[0][0])

    return vec_index

#获取用户*商品喜好程度矩阵
def getUserItemProbability(user_count,item_count,user_item,item_item,k):
    '''
    :param user_count:
    :param item_count:
    :param user_item:
    :param item_item:
    :param k: 最相似的k个物品
    :return:
    '''

    user_item_pro = np.zeros((user_count, item_count))
    for u in range(user_count):
        for i in range(item_count):
            N = getUserLike(user_item[u,:])
            S = getSimilarKItem(item_item[i,:],k)
            print(N)
            print(S)
            print("-----")
            intersect = list(set(N)&set(S))
            for a in range(len(intersect)):
                user_item_pro[u][i]=user_item_pro[u][i]+item_item[i][a]*user_item[u][a]

    return user_item_pro

if __name__ =="__main__":

    # 建立物品列表,index代表id
    items = ['冷冻肉', '鱼', '鲜肉', '甜食', '牛奶', '啤酒', '蔬菜水果', '饮料', '罐装肉', '葡萄酒', '罐装蔬菜']
    item_count = len(items)

    data = loadData("../data/data.xlsx",cols=['user_id','item','count','price','cash'])

    # 获取用户列表id,并进行排序,index代表用户id
    users = sorted(list(set(data['user_id'].astype("int"))))
    user_count = len(users)

    # 获取user_item,存储的值是rating
    user_item = getUserItem(user_count, item_count, users, items)
    #print(user_item)
    #print(user_item[:,0])

    # 获取item_item，存储的值是相似度
    item_item = getItemItem(item_count,user_item)
    #print(item_item)

    # 获取user_item_pro
    k=9
    user_item_pro = getUserItemProbability(user_count,item_count,user_item,item_item,k)

    print(user_item_pro.shape)


    np.save("./model.txt",user_item_pro)
    # 开始进行推荐
    # 输入需要推荐的用户id
    some_user = 1
    recommend_count = 1
    # 获取商品列表
    some_user_items = user_item_pro[some_user,:]
    max_pro = np.max(some_user_items)
    max_pro_index = np.argwhere(some_user_items==max_pro)
    print("用户===》",users[some_user])
    print("推荐商品==》",items[max_pro_index[0][0]])








