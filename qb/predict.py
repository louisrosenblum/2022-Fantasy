import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.linear_model import SGDClassifier
from sklearn.utils import shuffle
from sklearn.utils import shuffle
import matplotlib.pyplot as plt
from matplotlib import style
import pickle
import csv
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

# Import training data
train_data = pd.read_csv("train.csv", sep=",")

train_data = train_data.fillna(0)

columns = train_data.columns[2:]

predict = 'Next Year Fantasy Points'

X = np.array(train_data.drop([predict], 1)) # Features
y = np.array(train_data[predict]) # Labels

# Import testing data
test_data = pd.read_csv("test.csv", sep=",")

test_data = test_data.fillna(0)

x_test = np.array(test_data)

# Use Least Angle Regression
reg = linear_model.LassoCV(max_iter=100000)

xdel = np.delete(X,0,1)

xdel2 = np.delete(x_test,0,1)

# Apply standard scaler to the datasets
sc = StandardScaler()
sc.fit(xdel)

X_train_std = sc.transform(xdel)
X_test_std = sc.transform(xdel2)

reg.fit(X_train_std,y)

predictions = reg.predict(X_test_std)

with open('qb.csv', mode='w') as flex:
    writer = csv.writer(flex, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,lineterminator = '\n')

    for x in range(len(predictions)):
        writer.writerow([x_test[x][0],predictions[x]])

cdf = pd.DataFrame(reg.coef_, columns, columns=['Coefficients'])

cdf.to_csv('coefficients.csv')

print(reg.intercept_)

