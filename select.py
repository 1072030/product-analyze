import os
import numpy as np
import pandas as pd 

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
target_Item = {}
# 放分割好的單字(不分商品)
target_Split = []
# 放分割好的單字(分商品)
target_Split_Item = []
# 放所有包含"顯示卡","GPU"的category's rows
target_category_total = []
# 放所有包含"顯示卡","GPU"的price's rows
target_Price_total = []

# 將所有取到的value放入target_Item
for i in all_file_name:
    with open( dir_path+'\goods\\'+ i,"r",encoding="utf-8") as keyName:
        for i in keyName:
            #print(i)
            if is_in(i,target_Text):
                temp = i.split(",")
                target_Item["name"].append(temp[4])
                target_Item["category"].append(temp[0])
                target_Item["Price"].append(temp[3])

print(target_Item)