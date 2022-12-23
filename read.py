import pandas as pd
import numpy as np
import json
import os
import jieba as jb #https://www.youtube.com/watch?v=HGPPoaBxyb0&ab_channel=%E7%90%86%E5%BE%8B%E6%96%87%E6%95%99%E5%9F%BA%E9%87%91%E6%9C%83
import re #https://ithelp.ithome.com.tw/articles/10268012
import matplotlib.pyplot as plt
goods_path = os.path.dirname(os.path.realpath(__file__))
goods_file = os.listdir(goods_path+"/goods")
print(goods_file)
target_Text = ["PCI顯示卡","顯示卡","GPU","影片配接器","圖形卡","繪圖卡"]
target_Count = {"PCI顯示卡":0,"顯示卡":0,"GPU":0,"影片配接器":0,"圖形卡":0,"繪圖卡":0}
target_Item = {}
target_Price=[]
# 放分割好的單字(不分商品)
def is_in(full_str, sub_str):
    try:
        for i in range(len(sub_str)):
            if sub_str[i] in full_str:
                target_Count[sub_str[i]]+=1
                return True
    except ValueError:
        return False
category = {}
for i in range(goods_file.__len__()):
    goods = open('goods/'+goods_file[i], 'r',encoding="utf-8")
    data = pd.DataFrame(goods)
    for j in range(data.__len__()):
        good = json.loads(data[0][j])
        good['item_name'] = good['item_name'].replace('"','')
        good['item_name'] = good['item_name'].replace("'","")
        good['item_name'] = good['item_name'].replace(' ','')
        good['item_name'] = good['item_name'].replace('\\','')
        good['item_name'] = good['item_name'].replace("/","")
        good['item_name'] = good['item_name'].replace("◎","")
        good['item_name'] = good['item_name'].replace("[","")
        good['item_name'] = good['item_name'].replace("]","")
        good['item_name'] = good['item_name'].replace("@","")
        good['item_name'] = good['item_name'].replace("(","")
        good['item_name'] = good['item_name'].replace(")","")
        good['item_name'] = good['item_name'].replace("【","")
        good['item_name'] = good['item_name'].replace("】","")
        good['item_name'] = good['item_name'].replace("《","")
        good['item_name'] = good['item_name'].replace("》","")
        good['item_name'] = good['item_name'].replace("◢","")
        good['item_name'] = good['item_name'].replace("◣","")
        good['item_name'] = good['item_name'].replace("「","")
        good['item_name'] = good['item_name'].replace("」","")
        good['item_name'] = good['item_name'].replace("（","")
        good['item_name'] = good['item_name'].replace("）","")
        good['item_name'] = good['item_name'].replace("{","")
        good['item_name'] = good['item_name'].replace("}","")
        good['item_name'] = good['item_name'].replace(".","")
        good['item_name'] = good['item_name'].replace("。","")
        good['item_name'] = good['item_name'].replace("☆","")
        good['item_name'] = good['item_name'].replace("*","")
        good['item_name'] = good['item_name'].replace("~","")
        good['item_name'] = good['item_name'].replace("『","")
        good['item_name'] = good['item_name'].replace("』","")
        good['item_name'] = good['item_name'].replace("!","")
        good['item_name'] = good['item_name'].replace("&","")
        good['item_name'] = good['item_name'].replace("#","")
        good['item_name'] = good['item_name'].replace("�","")
        good['item_name'] = good['item_name'].replace("|","")
        good['item_name'] = good['item_name'].replace("←","")
        good['item_name'] = good['item_name'].replace("●","")
        good['item_name'] = good['item_name'].replace("★","")
        good['item_name'] = good['item_name'].replace("〝","")
        good['item_name'] = good['item_name'].replace("〞","")
        good['item_name'] = good['item_name'].replace("㊣","")
        good['item_name'] = good['item_name'].replace("◤","")
        good['item_name'] = good['item_name'].replace("�","")
        good['item_name'] = good['item_name'].replace("╭","")
        good['item_name'] = good['item_name'].replace("＠","")
        good['item_name'] = good['item_name'].replace("<","")
        good['item_name'] = good['item_name'].replace("｛","")
        good['item_name'] = good['item_name'].replace("｝","")
        good['item_name'] = good['item_name'].replace("$","")
        good['item_name'] = good['item_name'].replace("＋","")
        good['item_name'] = good['item_name'].replace("+","")
        if is_in(good['item_name'],target_Text):
            target_Item[good['item_name']]=good['price']
            target_Price.append(good['price'])
            # target_Item[good['item_name']]+=1
    print(i)

print(target_Item)
print(target_Price)
print(target_Count)

    # print(good['item_name'])
    # if good['item_name'] not in category:
    #     category[good['item_name']]=0
    # if(good['item_name'] in category):
    #     category[good['item_name']]+=1
    # print(category)
# print(category)
# print(data[0][0])