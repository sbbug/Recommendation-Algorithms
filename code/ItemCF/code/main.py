
import numpy as np

if __name__ =="__main__":
    user_item_pro = np.load("./model.npy")
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