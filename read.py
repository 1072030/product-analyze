import pandas as pd
import numpy as np
import json
import os
import random
goods_path = os.path.dirname(os.path.realpath(__file__))
goods_file = os.listdir(goods_path+"/goods")
# print(goods_file)
target_Text = ["PCI顯示卡","顯示卡","GPU","影片配接器","圖形卡","繪圖卡"]
target_Count = {"PCI顯示卡":0,"顯示卡":0,"GPU":0,"影片配接器":0,"圖形卡":0,"繪圖卡":0}
target_Double_Text=["贈","送","充電","散熱膏"]
target_Double_Count={"贈":0,"送":0,"充電":0,"散熱膏":0}
target_Item = {}
target_Double_Item={}

# 放分割好的單字(不分商品)
def is_in(full_str, sub_str,double=0):
    try:
        if double ==0:
            for i in range(len(sub_str)):
                if sub_str[i] in full_str:
                    target_Count[sub_str[i]]+=1
                    return True
        else:
            for i in range(len(sub_str)):
                if sub_str[i] in full_str:
                    target_Double_Count[sub_str[i]]+=1
                    return True
    except ValueError:
        return False
for i in range(10):
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
        check =  is_in(good['item_name'],target_Text)
        if check:
            target_Item[good['item_name']]=[]
            target_Item[good['item_name']].append(good['category_name'])
            target_Item[good['item_name']].append(good['price'])

            
    print(i)
for i in target_Item:
    if is_in(i,target_Double_Text,1):
        target_Double_Item[i]=target_Item[i]


# print(target_Item)
# print(target_Double_Item)
# print(target_Count)
# print(target_Double_Count)
# print(target_Item.__len__())
for i in target_Double_Item:
    target_Item.pop(i,None)
category_names=[]
prices=[]
names=[]
# print(target_Item.__len__())
for i in target_Item:
    category_names.append(target_Item[i][0])
    prices.append(target_Item[i][1])
    names.append(i)
dk = pd.DataFrame({"names":names,"category_names":category_names,"prices":prices})
dk['isCorrect'] = 1
print(dk)
dk.to_csv('isCorrect.csv',sep='\t',encoding='utf-8')
