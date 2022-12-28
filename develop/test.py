import pandas as pd
# from pandas import DataFrame,Series
import numpy as np
import json
from pandarallel import pandarallel
# from pyspark.sql.types import ArrayType,IntegerType
import time
from glob import glob
import torch
# from torch import 
import torch
from torch.utils.data import Dataset, DataLoader, random_split
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import torch.nn.functional as F
import torch.nn.functional as func
from matplotlib import pyplot as plt
# import pandarallel

from pyspark import SparkConf, SparkContext


if __name__ == '__main__':

    from pyspark import pandas as ps

    start = time.time()
    pandarallel.initialize(progress_bar=True)
    pro_list=[]
    pro_word=[]
    # global pro_list=[]

    def get_word(w,pro_word)->list:
        # global pro_word
        # print(w)
        pro_word+=list(w)

        return pro_word

    def check_word(w:str,words:list,r_arr):
        import numpy as np
        # a = str(anda)
        # a.encode()
        r_arr_1 = np.zeros(len(words))
        # item = w
        # r_arr[:len(r_arr)]=[0] * (len(r_arr))
        # print(w)
        try:
            for word in w.split():
                r_arr_1[words.index(word)]+=1
        except Exception as e:
            print(str(e))
        # print(r_arr)
        return r_arr_1

    files = glob('./goods/part-r-00000')

    data = ps.read_json(files).to_pandas()

    import re
    punct = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{}~'   # `|` is not present here
    transtab = str.maketrans(dict.fromkeys(punct, ''))

    data.iloc[:,["item_name"]] = data[data["category_name"]=="電腦周邊"].item_name.apply(lambda w:re.sub('\W',' ',w)).str.translate(transtab).str.lower()
    pro_list = data.item_name.str.split(" ")
    for w in pro_list:
        pro_word+=list(w)
    pro_word=pd.Series(pro_word).drop_duplicates().to_list()
    r_arr = np.zeros(len(pro_word)).tolist()
    # data["word_arr"] = data.item_name.parallel_apply(lambda w : r_arr[pro_word.index(w.split())]+=1 if (w.split() in pro_word) else pass)
    # s=0
    data_list=[]
    # data_list = pd.DataFrame([])
    clust=len(data)/4
    for i in range(4):
        data_list.append(data[int(round((i)*clust+0.5,0)):int(round((i+1)*clust+0.5,0))].item_name.parallel_apply(check_word,args=(pro_word,r_arr,)))
        # s=i
        
    data_1=pd.concat(data_list)

    pro_word_s=pd.Series(pro_word).drop_duplicates()
    pro_word_s_l = pro_word_s.tolist()

    r_arr = np.zeros(len(pro_word_s_l)).tolist()
    word_arr= data.item_name.transform(lambda w:check_word(w,pro_word_s_l,r_arr))
    data["word_arr"] = word_arr

    class MyDataset(Dataset):
    
        def __init__(self,data):
        
            word_arr = data.word_arr.values
            category = data.category_name.values
            self.word_arr=torch.tensor(word_arr,dtype=torch.float32)
            self.category=torch.tensor(category,dtype=torch.float32)
        
        def __len__(self):
            return len(self.category)
        
        def __getitem__(self,idx):
            return self.word_arr[idx],self.category[idx]

    transform = transforms.Compose(
        [transforms.ToTensor(),
        transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))])

    batch_size = 4

    train_dataset = MyDataset(data)

    train_set,val_set=random_split(train_dataset,[int(len(train_dataset)*0.7),len(train_dataset)-int(len(train_dataset)*0.7)],generator=torch.Generator().manual_seed(0))

    im, category = train_set[0]
    im = im.numpy()
    mask = category.numpy()
    prod = np.multiply(im, mask)
    print(prod.shape)
    plt.figure()
    plt.imshow(prod[0])
    plt.show()



    class Net(nn.Module):
        def __init__(self) :

            super(Net, self).__init__()
            self.conv1 = nn.Conv2d(1, 3, kernel_size=5)
            self.conv2 = nn.Conv2d(3, 9, kernel_size=5)
            self.fc1 = nn.Linear(9*5*5, 120)
            self.fc2 = nn.Linear(120, 84)
            self.fc3 = nn.Linear(84, 10)

        def forward (self, x) :
            x = func.relu(self.conv1(x) )
            x = func.max_pool2d(x,2)
            x = func.relu(self.conv2(x) )
            x = func.max_pool2d(x,2)
            x = x.view(x.size(0), -1)
            x = func.relu(self.fc1(x))
            x = func.relu(self.fc2(x) )
            x = self.fc3(x)
            return x

    net=Net()
    # print(net)
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    net.to(device) 

    import torch.optim as optim
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(),lr=0.001,momentum=0.9)

    print(time.time()-start)

    pass