import operator
import math

# train 格式 ：{user:{item:rating}}
def user_similarity(train):
    item_users = dict()
    for u, items in train.items():
        for i in items.keys():
            if i not in item_users:
                item_users[i] = set()
            item_users[i].add(u)

    # 计算相似user共同的物品数量
    C = dict() #共同用户之间相同物品的数量 用户对相同电影评价的数量 交集
    N = dict() #存储每个用户拥有的item数量 用户评价过的电影的数量 分母
    for i, users in item_users.items():
        for u in users:
            if N.get(u, -1) == -1:
                N[u] = 0
            N[u] += 1
            if C.get(u, -1) == -1:
                C[u] = dict()
            for v in users:
                if u == v:
                    continue
                elif C[u].get(v, -1) == -1:
                    C[u][v] = 0
                C[u][v] += 1

    # 得到最终的相似度矩阵W
    W = dict()
    for u, related_users in C.items():
        if W.get(u, -1) == -1:
            W[u] = dict()
        for v, cuv in related_users.items():
            W[u][v] = cuv / math.sqrt(N[u] * N[v] * 1.0)
    return W

### 相似用户的物品集合
def recommend(user, train, w, k):
    rank = dict()
    interactor_items = train[user].keys()