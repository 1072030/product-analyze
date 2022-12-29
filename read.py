import pandas as pd
import numpy as np
import json
import os
import random
import jieba
import jieba.analyse
import jieba.posseg as pseg  #使用pseq進行詞性標記
jieba.enable_parallel()
jieba.case_sensitive = True
dir_path = os.path.dirname(os.path.realpath(__file__))

goods_file = os.listdir(dir_path+"/goods")
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
# goods_file.__len__()
for i in range(0):
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
        # print("|".join(jieba.cut(good['item_name'],cut_all=True,HMM=True)))
        check =  is_in(good['item_name'],target_Text)
        if check:
            target_Item[good['item_name']]=[]
            target_Item[good['item_name']].append(good['category_name'])
            target_Item[good['item_name']].append(good['price'])

            
    print(i)
for i in target_Item:
    if is_in(i,target_Double_Text,1):
        target_Double_Item[i]=target_Item[i]

for i in target_Double_Item:
    target_Item.pop(i,None)

words={"word":[]}
print("saving as json file : word.json")
# for i in target_Item:
#     words["word"].append(i)
# json_words = json.dumps(words,indent=4,ensure_ascii=False)
# with open("word.json","w",encoding="utf8") as outfile:
#     outfile.write(json_words)
category_names=[]
prices=[]
names=[]



for i in target_Item:
    category_names.append(target_Item[i][0])
    prices.append(target_Item[i][1])
    names.append(i)
dk = pd.DataFrame({"names":names,"category_names":category_names,"prices":prices})
dk['isCorrect'] = 1
print(dk)
dk.to_csv('isCorrect.csv',sep='\t',encoding='utf-8')



with open("word.json", 'r',encoding="utf-8") as jsonfile:
    data_json = json.load(jsonfile)
    all_word=""
    symbol = ","

    #設定testing set
    # test_json = json.dumps(data["word"][:1000],indent=4,ensure_ascii=False)
    # with open("test.json",'w',encoding="utf8") as test:
    #     test.write(test_json)

    # # 原data刪除testing data
    # del data["word"][:1000]

    #新增traing set
    train_json = json.dumps(data_json["word"],indent=4,ensure_ascii=False)
    with open("train.json",'w',encoding="utf8") as test:
        data = pd.DataFrame(data_json)
        data['isCorrect']=1
        # print(data)
        test.write(train_json)
    temp = pd.read_csv('./data/train_Data.csv')
    temp2 = pd.read_csv('./data/test_data.csv')
    temp = pd.DataFrame(temp)
    temp2 = pd.DataFrame(temp2)
    train_csv_rebuild = temp.drop(['B','C'],axis=1)
    test_csv_rebuild = temp2.drop(['B','C'],axis=1)
    train_csv_rebuild.to_csv('tfid_trainingSet.csv',sep='\t',encoding='utf-8')
    test_csv_rebuild.to_csv('tfid_testingSet.csv',sep='\t',encoding='utf-8')
    
    all_word=symbol.join(data["word"])
    print("jieba calculating~!")
    jieba.analyse.set_stop_words("unSupport.txt")
    tags = jieba.analyse.extract_tags(all_word,withWeight=True,topK=20) #TF-IDF權重
    # print(tags)
#-----------------------------------------------start training
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import accuracy_score
from scipy.sparse import coo_matrix
# from xgboost import XGBClassifier
stoplist = list(pd.read_table("unSupport.txt",names=["w"],sep='aaa',encoding="utf-8",engine="python").w)
def m_cut(txt):
    return [w for w in jieba.lcut(txt) if w not in stoplist and len(w)>1]
with open('train.json','r',encoding="utf8") as trainset:
    trainSet = json.load(trainset)
    # print(trainSet)
    trainData=""
    for i in range(trainSet.__len__()):
        trainData+=trainSet[i]
        trainData+=","
    # print(trainData)
    txt_list=[" ".join(m_cut(trainData))]
    # print(txt_list)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(txt_list)
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(X)
    word=vectorizer.get_feature_names_out()
    weight=tfidf.toarray()
    data_dict={}
    for i in range(len(weight)):
        for j in range(len(word)):
            data_dict[word[j]]=weight[i,j]
    print(sorted(data_dict.items(),key=lambda x:x[1],reverse=True)[:10])
    # print(weight[:10])


