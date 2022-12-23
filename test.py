import os
import numpy as np
import pandas as pd 
dir_path = os.path.dirname(os.path.realpath(__file__))
#↑獲取當前資料夾名稱然後存成dir_path變數

all_file_name = os.listdir(dir_path+"/goods")
print(all_file_name)
#↑讀取資料夾內所有檔案名稱然後放進all_file_name這個list裡

all_file_name.pop(0)
all_file_name.pop(0)
target_Text = ["顯示卡","GPU"]

def is_in(full_str, sub_str):
    try:
        for i in range(len(sub_str)):
            full_str.index(sub_str[i])
            return True
    except ValueError:
        return False

# 放所有包含"顯示卡","GPU"的rows
target_Item = []
# 放分割好的單字(不分商品)
target_Split = []
# 放分割好的單字(分商品)
target_Split_Item = []

# 將所有取到的value放入target_Item
for i in all_file_name:
    with open(i,"r",encoding="utf-8") as keyName:
        for i in keyName:
            #print(i)
            if is_in(i,target_Text):
                temp = i.split(",")
                target_Item.append(temp[4])

item_name = ["item_name"]

# 將切割的單字依照商品類別放入target_Split_Item
# 之後不分類將單字全部放入target_Split
for i in range(len(target_Item)):
    # 用空白分割資料
    tempArr = target_Item[i].split(" ")
    # 用:分開資料
    tempArr1 = tempArr[0].split(":")
    # tempArr第0位資料會和tempArr1重複所以刪除
    tempArr.pop(0)
    # 最後組合兩個Array
    tempTotal = tempArr1 + tempArr
    
    # 刪除含有item_name的元素
    tempTotal.pop(0)
    
    # 刪除資料中一些符號
    for i in range(len(tempTotal)):
        tempTotal[i] = tempTotal[i].replace('"','')
        tempTotal[i] = tempTotal[i].replace("'","")
        tempTotal[i] = tempTotal[i].replace(' ','')
        tempTotal[i] = tempTotal[i].replace('\\','')
        tempTotal[i] = tempTotal[i].replace("/","")
        tempTotal[i] = tempTotal[i].replace("◎","")
        tempTotal[i] = tempTotal[i].replace("[","")
        tempTotal[i] = tempTotal[i].replace("]","")
        tempTotal[i] = tempTotal[i].replace("@","")
        tempTotal[i] = tempTotal[i].replace("(","")
        tempTotal[i] = tempTotal[i].replace(")","")
        tempTotal[i] = tempTotal[i].replace("【","")
        tempTotal[i] = tempTotal[i].replace("】","")
        tempTotal[i] = tempTotal[i].replace("《","")
        tempTotal[i] = tempTotal[i].replace("》","")
        tempTotal[i] = tempTotal[i].replace("◢","")
        tempTotal[i] = tempTotal[i].replace("◣","")
        tempTotal[i] = tempTotal[i].replace("「","")
        tempTotal[i] = tempTotal[i].replace("」","")
        tempTotal[i] = tempTotal[i].replace("（","")
        tempTotal[i] = tempTotal[i].replace("）","")
        tempTotal[i] = tempTotal[i].replace("{","")
        tempTotal[i] = tempTotal[i].replace("}","")
        tempTotal[i] = tempTotal[i].replace(".","")
        tempTotal[i] = tempTotal[i].replace("。","")
        tempTotal[i] = tempTotal[i].replace("☆","")
        tempTotal[i] = tempTotal[i].replace("*","")
        tempTotal[i] = tempTotal[i].replace("~","")
        tempTotal[i] = tempTotal[i].replace("『","")
        tempTotal[i] = tempTotal[i].replace("』","")
        tempTotal[i] = tempTotal[i].replace("!","")
        tempTotal[i] = tempTotal[i].replace("&","")
        tempTotal[i] = tempTotal[i].replace("#","")
        tempTotal[i] = tempTotal[i].replace("�","")
        tempTotal[i] = tempTotal[i].replace("|","")
        tempTotal[i] = tempTotal[i].replace("←","")
        tempTotal[i] = tempTotal[i].replace("●","")
        tempTotal[i] = tempTotal[i].replace("★","")
        tempTotal[i] = tempTotal[i].replace("〝","")
        tempTotal[i] = tempTotal[i].replace("〞","")
        tempTotal[i] = tempTotal[i].replace("㊣","")
        tempTotal[i] = tempTotal[i].replace("◤","")
        tempTotal[i] = tempTotal[i].replace("�","")
        tempTotal[i] = tempTotal[i].replace("╭","")
        tempTotal[i] = tempTotal[i].replace("＠","")
        tempTotal[i] = tempTotal[i].replace("<","")
        tempTotal[i] = tempTotal[i].replace("｛","")
        tempTotal[i] = tempTotal[i].replace("｝","")
        tempTotal[i] = tempTotal[i].replace("$","")
        tempTotal[i] = tempTotal[i].replace("＋","")
        tempTotal[i] = tempTotal[i].replace("+","")
        
        if i == None:
            tempTotal.remove(i)
    
    # 已刪除含有item_name的陣列append到target_Split_Item(分商品)
    target_Split_Item.append(tempTotal)
    
    # 已刪除含有item_name的陣列append到target_Split(不分商品)
    for j in tempTotal:
        target_Split.append(j)

# 刪除重複的值
target_Split = list(set(target_Split))

print(target_Split)
print(len(target_Split))
#print(target_Split)