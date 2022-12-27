# data processing, CSV file I/O (e.g. pd.read_csv)
import pandas as pd 

# import os function
import os 

# Modeling and Predicting
from sklearn.tree import DecisionTreeClassifier


goods_path = os.path.dirname(os.path.realpath(__file__))

train_data = pd.read_csv(goods_path+'isCorrect.xlsx')
test_data = pd.read_csv('../input/bigdata/test.csv')

train_data.isnull().sum() #checking for Null values

#checking:
train_data.head()

#Spliting train data into X (features) and y (answear):
y = train_data['isCorrect']
X = train_data.drop(['isCorrect'], axis=1)

#We don't need to do this with test_data because test_data has no answears, only features.

#here you can change our model parameters such as max_depth or random_state
model = DecisionTreeClassifier(max_depth=4)
model.fit(X, y)
train_data.head()

# Prediction of target for test data
preds = model.predict(test_data).astype(int)

# Saving the result into submission file
submission = pd.read_csv('../input/bigdata/ex_submit.csv')
submission["Attribute17"] = preds
submission.to_csv('ex_submit.csv', index=False) # Competition rules require that no index number be saved