# data processing, CSV file I/O (e.g. pd.read_csv)
import pandas as pd 

# import os function
import os 

# Modeling and Predicting
from sklearn.tree import DecisionTreeClassifier


goods_path = os.path.dirname(os.path.realpath(__file__))

# error_bad_lines=False
train_data = pd.read_csv(goods_path+'\\train_Data.csv', 'r', encoding="utf-8", error_bad_lines=False)
test_data = pd.read_csv(goods_path+'\\isCorrect.csv', 'r', encoding="utf-8", error_bad_lines=False)

train_data.isnull().sum() #checking for Null values

#checking:
print(train_data.head())

#Spliting train data into X (features) and y (answear):
y = train_data['D']
X = train_data.drop(['D'], axis=1)

#We don't need to do this with test_data because test_data has no answears, only features.

#here you can change our model parameters such as max_depth or random_state
model = DecisionTreeClassifier(max_depth=4)
model.fit(X, y)
train_data.head()

# Prediction of target for test data
preds = model.predict(test_data).astype(int)

# Saving the result into submission file
submission = pd.read_csv('../input/bigdata/result.csv')
submission["isCorrect"] = preds
submission.to_csv('result.csv', index=False) # Competition rules require that no index number be saved