import pandas as pd
import numpy as np
import json
import os
import random

dir_path = os.path.dirname(os.path.realpath(__file__))
#↑獲取當前資料夾名稱然後存成dir_path變數

all_file_name = os.listdir(dir_path+"\goods")
#↑讀取資料夾內所有檔案名稱然後放進all_file_name這個list裡
# all_file_name.pop(0)
# all_file_name.pop(-1)

target_Text = ["顯示卡"]

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
# 放所有包含"顯示卡","GPU"的category's rows
target_category = []
# 放所有包含"顯示卡","GPU"的price's rows
target_Price = []
# 分數欄位
score = []
score1 = []
# 非GPU
other_Item = []
other_Category = []
other_Price = []
other_Split_Item = []

# punct = '!"#$%&\'()*+-./:;<=>?@[\\]^_`{}~【】◎'   # `|` is not present here
# transtab = str.maketrans(dict.fromkeys(punct, ''))
# data['item_name'] = data['item_name'].str.lower().str.translate(transtab)
replace_Txt = '"\'\\/[]{}｛｝【】()（）@!"#$%&\'()*+-./:;<=>?@[\\]^_`~【】◎『』'
transtab = str.maketrans(dict.fromkeys(replace_Txt, ''))

# 將所有取到的value放入target_Item
for i in all_file_name:
    with open( dir_path+'\goods\\'+ i,"r",encoding="utf-8") as keyName:
        for i in keyName:
            #print(i)
            if is_in(i,target_Text):
                temp = i.split(",")
                target_Item.append(temp[4])
                target_category.append(temp[0])
                target_Price.append(temp[3])
            else:    
                if(len(other_Item)<6686):
                    temp1 = i.split(",")
                    other_Item.append(temp1[4])
                    other_Category.append(temp1[0])
                    other_Price.append(temp1[3])
                
                

for i in range(len(target_Item)):
    # 以:分割
    # GPU
    tempTar = target_Item[i].split(":")
    tempCat = target_category[i].split(":")
    tempPri = target_Price[i].split(":")
    # not GPU
    tempOI = other_Item[i].split(":")
    tempOC = other_Category[i].split(":")
    tempOP = other_Price[i].split(":")
    # GPU
    tempTar.pop(0)
    tempCat.pop(0)
    tempPri.pop(0)
    # not GPU
    tempOI.pop(0)
    tempOC.pop(0)
    tempOP.pop(0)
    # GPU
    target_Item[i] = tempTar
    target_category[i] = tempCat
    target_Price[i] = tempPri
    # not GPU
    other_Item[i] = tempOI
    other_Category[i] = tempOC
    other_Price[i] = tempOP

# GPU處理價格和種類文字
for k in range(len(target_Price)):
    a = ' '.join(target_Price[k])
    #print(a)
    a = a.translate(transtab)
    target_Price[k] = a
    #print(target_Price[k])
    
    aa = ' '.join(target_category[k])
    #print(aa)
    aa = aa.translate(transtab)
    target_category[k] = aa
    #print(target_category[k])
    
    b = ' '.join(other_Price[k])
    #print(a)
    b = b.translate(transtab)
    other_Price[k] = b
    
    bb = ' '.join(other_Category[k])
    #print(aa)
    bb = bb.translate(transtab)
    other_Category[k] = bb
    


# GPU將整個單字依照商品區分
for j in range(len(target_Item)):
    a = str(target_Item[j]).split(" ")
    b = ' '.join(a)
    b = b.translate(transtab)
    c = b.split(' ')
    while '' in c:
        c.remove('')
    target_Split_Item.append(c)
    # 不依照商品類別區分
    target_Split.extend(c)
    
    aa = str(other_Item[j]).split(" ")
    bb = ' '.join(aa)
    bb = bb.translate(transtab)
    cc = bb.split(' ')
    while '' in cc:
        cc.remove('')
    other_Split_Item.append(cc)
    
print(target_Split)

# 分商品的總長度
for totallen in range(len(target_Split_Item)):
    count = 0
    count1 = 0
    # 氛商品中元素長度
    for itemlen in range(len(target_Split_Item[totallen])):
        # 不分商品的總長度
        for alllen in target_Split:
            if target_Split_Item[totallen][itemlen] == alllen:
                count+=1
    for otheritemlen in range(len(other_Split_Item[totallen])):
        for alllen in target_Split:
            if other_Split_Item[totallen][otheritemlen] == alllen:
                count1+=1
    
                       
    
    score.append(count)
    score1.append(count1)

dk = pd.DataFrame({"score":score,"category_names":target_category,"prices":target_Price})
dk["isCorrect"] = 1
dk.to_csv('newDataGPU.csv',sep='\t',encoding='utf-8')

dk1 = pd.DataFrame({"score":score1,"category_names":other_Category,"prices":other_Price})
dk1["isCorrect"] = 0
dk1.to_csv('newDataNotGPU.csv',sep='\t',encoding='utf-8')
# print(target_Item)
# print(target_Item.__len__())
print(len(score))

# print(target_Price)
# print(target_Item.__len__())
# print(target_category.__len__())
# print(target_Price.__len__())




# # 將切割的單字依照商品類別放入target_Split_Item
# # 之後不分類將單字全部放入target_Split
# for i in range(len(target_Item)):
#     count = 0
#     # 用空白分割資料
#     tempArr = target_Item[i].split(" ")
#     tempArrCate = target_category[i].split(" ")
#     # 用:分開資料
#     tempArr1 = tempArr[0].split(":")
#     tempArrCate1 = tempArrCate[0].split(":")
#     target_Price1 = target_Price[i].split(":")
#     # tempArr第0位資料會和tempArr1重複所以刪除
#     tempArr.pop(0)
#     tempArrCate1.pop(0)
#     target_Price1.pop(0)
    
#     # 最後組合兩個Array
#     tempTotal = tempArr1 + tempArr
    
#     # 刪除含有item_name的元素
#     tempTotal.pop(0)
    
#     for i in range(len(target_Price1)):
#         target_Price1[i] = target_Price1[i].replace('"','')
#         if i == None:
#             target_Price1.remove(i)
    
#     # 刪除資料中一些符號
    # for i in range(len(tempTotal)):
    #     tempTotal[i] = tempTotal[i].replace('"','')
    #     tempTotal[i] = tempTotal[i].replace("'","")
    #     tempTotal[i] = tempTotal[i].replace(' ','')
    #     tempTotal[i] = tempTotal[i].replace('\\','')
    #     tempTotal[i] = tempTotal[i].replace("/","")
    #     tempTotal[i] = tempTotal[i].replace("◎","")
    #     tempTotal[i] = tempTotal[i].replace("[","")
    #     tempTotal[i] = tempTotal[i].replace("]","")
    #     tempTotal[i] = tempTotal[i].replace("@","")
    #     tempTotal[i] = tempTotal[i].replace("(","")
    #     tempTotal[i] = tempTotal[i].replace(")","")
    #     tempTotal[i] = tempTotal[i].replace("【","")
    #     tempTotal[i] = tempTotal[i].replace("】","")
    #     tempTotal[i] = tempTotal[i].replace("《","")
    #     tempTotal[i] = tempTotal[i].replace("》","")
    #     tempTotal[i] = tempTotal[i].replace("◢","")
    #     tempTotal[i] = tempTotal[i].replace("◣","")
    #     tempTotal[i] = tempTotal[i].replace("「","")
    #     tempTotal[i] = tempTotal[i].replace("」","")
    #     tempTotal[i] = tempTotal[i].replace("（","")
    #     tempTotal[i] = tempTotal[i].replace("）","")
    #     tempTotal[i] = tempTotal[i].replace("{","")
    #     tempTotal[i] = tempTotal[i].replace("}","")
    #     tempTotal[i] = tempTotal[i].replace(".","")
    #     tempTotal[i] = tempTotal[i].replace("。","")
    #     tempTotal[i] = tempTotal[i].replace("☆","")
    #     tempTotal[i] = tempTotal[i].replace("*","")
    #     tempTotal[i] = tempTotal[i].replace("~","")
    #     tempTotal[i] = tempTotal[i].replace("『","")
    #     tempTotal[i] = tempTotal[i].replace("』","")
    #     tempTotal[i] = tempTotal[i].replace("!","")
    #     tempTotal[i] = tempTotal[i].replace("&","")
    #     tempTotal[i] = tempTotal[i].replace("#","")
    #     tempTotal[i] = tempTotal[i].replace("�","")
    #     tempTotal[i] = tempTotal[i].replace("|","")
    #     tempTotal[i] = tempTotal[i].replace("←","")
    #     tempTotal[i] = tempTotal[i].replace("●","")
    #     tempTotal[i] = tempTotal[i].replace("★","")
    #     tempTotal[i] = tempTotal[i].replace("〝","")
    #     tempTotal[i] = tempTotal[i].replace("〞","")
    #     tempTotal[i] = tempTotal[i].replace("㊣","")
    #     tempTotal[i] = tempTotal[i].replace("◤","")
    #     tempTotal[i] = tempTotal[i].replace("�","")
    #     tempTotal[i] = tempTotal[i].replace("╭","")
    #     tempTotal[i] = tempTotal[i].replace("＠","")
    #     tempTotal[i] = tempTotal[i].replace("<","")
    #     tempTotal[i] = tempTotal[i].replace("｛","")
    #     tempTotal[i] = tempTotal[i].replace("｝","")
    #     tempTotal[i] = tempTotal[i].replace("$","")
    #     tempTotal[i] = tempTotal[i].replace("＋","")
    #     tempTotal[i] = tempTotal[i].replace("+","")
        
#         if i == None:
#             tempTotal.remove(i)
    
#     for i in range(len(tempArrCate1)):
#         tempArrCate1[i] = tempArrCate1[i].replace('"','')
#         tempArrCate1[i] = tempArrCate1[i].replace("'","")
#         tempArrCate1[i] = tempArrCate1[i].replace(' ','')
#         tempArrCate1[i] = tempArrCate1[i].replace('\\','')
#         tempArrCate1[i] = tempArrCate1[i].replace("/","")
#         tempArrCate1[i] = tempArrCate1[i].replace("◎","")
#         tempArrCate1[i] = tempArrCate1[i].replace("[","")
#         tempArrCate1[i] = tempArrCate1[i].replace("]","")
#         tempArrCate1[i] = tempArrCate1[i].replace("@","")
#         tempArrCate1[i] = tempArrCate1[i].replace("(","")
#         tempArrCate1[i] = tempArrCate1[i].replace(")","")
#         tempArrCate1[i] = tempArrCate1[i].replace("【","")
#         tempArrCate1[i] = tempArrCate1[i].replace("】","")
#         tempArrCate1[i] = tempArrCate1[i].replace("《","")
#         tempArrCate1[i] = tempArrCate1[i].replace("》","")
#         tempArrCate1[i] = tempArrCate1[i].replace("◢","")
#         tempArrCate1[i] = tempArrCate1[i].replace("◣","")
#         tempArrCate1[i] = tempArrCate1[i].replace("「","")
#         tempArrCate1[i] = tempArrCate1[i].replace("」","")
#         tempArrCate1[i] = tempArrCate1[i].replace("（","")
#         tempArrCate1[i] = tempArrCate1[i].replace("）","")
#         tempArrCate1[i] = tempArrCate1[i].replace("{","")
#         tempArrCate1[i] = tempArrCate1[i].replace("}","")
#         tempArrCate1[i] = tempArrCate1[i].replace(".","")
#         tempArrCate1[i] = tempArrCate1[i].replace("。","")
#         tempArrCate1[i] = tempArrCate1[i].replace("☆","")
#         tempArrCate1[i] = tempArrCate1[i].replace("*","")
#         tempArrCate1[i] = tempArrCate1[i].replace("~","")
#         tempArrCate1[i] = tempArrCate1[i].replace("『","")
#         tempArrCate1[i] = tempArrCate1[i].replace("』","")
#         tempArrCate1[i] = tempArrCate1[i].replace("!","")
#         tempArrCate1[i] = tempArrCate1[i].replace("&","")
#         tempArrCate1[i] = tempArrCate1[i].replace("#","")
#         tempArrCate1[i] = tempArrCate1[i].replace("�","")
#         tempArrCate1[i] = tempArrCate1[i].replace("|","")
#         tempArrCate1[i] = tempArrCate1[i].replace("←","")
#         tempArrCate1[i] = tempArrCate1[i].replace("●","")
#         tempArrCate1[i] = tempArrCate1[i].replace("★","")
#         tempArrCate1[i] = tempArrCate1[i].replace("〝","")
#         tempArrCate1[i] = tempArrCate1[i].replace("〞","")
#         tempArrCate1[i] = tempArrCate1[i].replace("㊣","")
#         tempArrCate1[i] = tempArrCate1[i].replace("◤","")
#         tempArrCate1[i] = tempArrCate1[i].replace("�","")
#         tempArrCate1[i] = tempArrCate1[i].replace("╭","")
#         tempArrCate1[i] = tempArrCate1[i].replace("＠","")
#         tempArrCate1[i] = tempArrCate1[i].replace("<","")
#         tempArrCate1[i] = tempArrCate1[i].replace("｛","")
#         tempArrCate1[i] = tempArrCate1[i].replace("｝","")
#         tempArrCate1[i] = tempArrCate1[i].replace("$","")
#         tempArrCate1[i] = tempArrCate1[i].replace("＋","")
#         tempArrCate1[i] = tempArrCate1[i].replace("+","")
    
#         if i == None:
#             tempArrCate1.remove(i)
    
#     # 新增分類的欄位
#     for i in range(len(tempTotal)):
#         target_category_total.append(tempArrCate1)
        
#     # 已刪除含有item_name的陣列append到target_Split_Item(分商品)
#     target_Split_Item.append(tempTotal)
    
#     # 已刪除含有item_name的陣列append到target_Split(不分商品)
#     for j in tempTotal:
#         target_Split.append(j)
        
#     for k in target_Price:
#         target_Price_total.append(k)
    
#     count+=1

# # 刪除重複的值
# target_Split = list(set(target_Split))


# # print(target_Split)
# print(target_Split_Item)

# score = []

# for totallen in range(len(target_Split)):
#     for itemlen in range(len(target_Split_Item)):
#         count = 0
#         for oneitemlen in range(len(target_Split_Item[itemlen])):
#             if target_Split_Item[itemlen][oneitemlen] == target_Split[totallen]:
#                 count += 1  
#         score.append(count)

# print(target_Split.__len__())
# print(target_Split_Item.__len__())
# print(score.__len__())
# print(target_category_total.__len__())
# print(target_Price_total.__len__())

# finalfile = {}

# finalfile["score"] = score
# finalfile["cate"] = tempArrCate1
# finalfile["price"] = target_Price1

# print(finalfile)

# print(len(target_Split))
# print(target_Split[0:10])
# print(len(target_category_total))
# print(target_category_total[0:300])
# print(target_Split)