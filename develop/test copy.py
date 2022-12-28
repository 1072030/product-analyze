import pandas as pd
# from pandas import DataFrame,Series
import numpy as np
import json
from pandarallel import pandarallel
# from pyspark.sql.types import ArrayType,IntegerType
import time
from glob import glob
# import torch
# # from torch import 
# import torch
# from torch.utils.data import Dataset, DataLoader, random_split
# import torch.nn as nn
# import torchvision
# import torchvision.transforms as transforms
# import torch.nn.functional as F
# import torch.nn.functional as func
from matplotlib import pyplot as plt
import os
# import pandarallel

from pyspark import SparkConf, SparkContext

# from multiprocessing import Pool
# I have 4 cores
# n_cores = 4

def find_other_category_count(gra_word_1,not_gra_card):
    # not_gra_card_size = 
    # global gra_word_df
    # global not_gra_card
    # print(gra_word_1)
    # print(not_gra_card.str.count(gra_word_1).sum())
    return not_gra_card.str.count(gra_word_1).sum()

# def find_graghic_card(product):
# # not_gra_card_size = 
# # global gra_word_df
# # global not_gra_card
# # print(gra_word_1)
# # print(not_gra_card.str.count(gra_word_1).sum())
#     if()
#     return not_gra_card.str.count(gra_word_1).sum()

if __name__ == '__main__':
    # global gra_word_df,not_gra_card
    # pool = Pool()

    from pyspark import pandas as ps

    start = time.time()
    pandarallel.initialize(progress_bar=True)
    
    pro_list=[]
    pro_word=[]
    # global pro_list=[]

    # def get_word(w,pro_word)->list:
    #     pro_word+=list(w)

    #     return pro_word

    # def check_word(w:str,words:list,r_arr):
    #     import numpy as np
    #     # a = str(anda)
    #     # a.encode()
    #     r_arr_1 = np.zeros(len(words))
    #     # item = w
    #     # r_arr[:len(r_arr)]=[0] * (len(r_arr))
    #     # print(w)
    #     try:
    #         for word in w.split():
    #             r_arr_1[words.index(word)]+=1
    #     except Exception as e:
    #         print(str(e))
    #     # print(r_arr)
    #     return r_arr_1

    # df_list=[]
    # for file in  glob('./data/*'):
    #     # files = glob(f'./goods/part-r-*{i}')
    #     # print(file.split("-"))
    #     data = pd.read_json(file)
    #     # data.to_json("data/"+file.split("-")[-1]+".json",orient="records",force_ascii=False)
    #     df_list.append(data)

    # data = pd.concat(df_list)
    # data.to_json("data/ALL_DATA.json",orient="records",force_ascii=False)

    # 建立商品Dataframe
    if os.path.exists("./data/ALL_DATA.json"):
        data = pd.read_json("./data/ALL_DATA.json")
    else:
        data = pd.read_json("../data/ALL_DATA.json")

    # 商品文字處理
    punct = '!"#$%&\'()*+-./:;<=>?@[\\]^_`{}~【】◎'   # `|` is not present here
    transtab = str.maketrans(dict.fromkeys(punct, ''))
    data['item_name'] = data['item_name'].str.lower().str.translate(transtab)

    # 取出商品名稱含'顯示卡'的商品
    gra = data[data['item_name'].str.contains('顯示卡')]
    # 統計各商品分類中出現'顯示卡'的次數
    gra_cate_count = gra["category_name"].value_counts()
    # 篩選掉'顯示卡'出現次數太少的分類
    gra_cate_count = gra_cate_count[gra_cate_count>5]
    gra_cate = gra_cate_count.index

    # 建立不是顯示卡的商品Dataframe
    not_gra_card = data[~data["category_name"].isin(gra_cate)]
    # 建立內建分類成顯示卡的商品Dataframe
    gra_card = data[data["category_name"]=="顯示卡"]

    # # gra_card = pd.read_json("顯示卡")

    # # 建立顯示卡分類中出現過的文字次數Dataframe
    # word = gra_card["item_name"].str.replace(","," ").str.split()
    # wr=[]
    # for w in word:
    #     wr.append(pd.Series(w))
    # word = pd.concat(wr)
    # gra_word = word.value_counts()
    # gra_word_df = pd.DataFrame(gra_word,columns=["gra_category_count"])
    # gra_word_df["other_category_count"]=0
    # gra_word_df['index1'] = gra_word_df.index
    
    # # 計算該文字出現在"不是"顯示卡分類的次數
    # gra_word_df["other_category_count"] = gra_word_df['index1'].parallel_apply(find_other_category_count,args=(not_gra_card['item_name'],))
    # gra_word_df.to_json("gra_word_df.json",orient="records",force_ascii=False)

    if os.path.exists("./gra_word_df.json"):
        gra_word_df = pd.read_json("./gra_word_df.json")
    else:
        gra_word_df = pd.read_json("../gra_word_df.json")

    #將文字出現在"不是"顯示卡分類的次數與出現在"是"顯示卡分類的次數做比值並過濾
    gra_word_df["graphic_card"] = gra_word_df.apply(lambda p: True if p["other_category_count"]/p["gra_category_count"] < 15 else False,axis=1)
    gra_card_def = gra_word_df[gra_word_df["graphic_card"]==True]

    # # 建立是顯示卡的商品Dataframe
    # gra_data = data[data["item_name"].str.contains("|".join(gra_card_def["index1"]),regex=True)]
    # gra_data.to_json("gra_data.json",orient="records",force_ascii=False)

    gra_data = pd.read_json("gra_data.json")
    a=1

    #將有出現該文字的商品作價格分析
    key_word = input("輸入顯示卡keyword : ")
    print(key_word)
    if key_word in gra_card_def["index1"].to_list():
        result = gra_data[gra_data["item_name"].str.contains(key_word)]
        result["price"].astype("float64").plot.hist(grid=True,
        color='#607c8e',xlim = [0,int(result["price"].max())],bins=result["price"].size)
        
        plt.show()
    else:
        print("This word isn't contained in graghic card")




    # gra_card["price"].astype('float32').plot.hist(grid=True,bins=1000,
    #                color='#607c8e',xlim=[0,100000])
    # gra_word_df.to_json("gra_word_df.json",orient="records",force_ascii=False)
    
    # gra_card["price"].plot.kde(grid=True,
    #         color='#607c8e',xlim=[0,100000])
    # print(gra_card["price"].value_counts())
    # # a=1
    # gra_card.to_json("顯示卡",orient="records",force_ascii=False)
    
  