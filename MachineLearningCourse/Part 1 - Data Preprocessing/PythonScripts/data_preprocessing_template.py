# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 14:54:19 2018

@author: Omar
"""

# Data Preprocessing

#Importing Libraries 

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

np.set_printoptions(threshold = np.nan)
# Importing the dataset
dataset = pd.read_csv('Data.csv')

x = dataset.iloc[:,:-1].values

y = dataset.iloc[:, 3].values

# Taking care of missing data
from sklearn.preprocessing import Imputer

imputer = Imputer(missing_values='NaN', strategy='median', axis=0)

imputer = imputer.fit(x[:, 1:3])

x[:, 1:3] = imputer.transform(x[:, 1:3])

# Encoding categorical data
# label encoder replaces strings or objects to numbers, only encodes values without order
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

lblEnc_x = LabelEncoder()

x[:, 0] = lblEnc_x.fit_transform(x[:, 0])

# categorizing data with order 


oneHtEnc_x = OneHotEncoder(categorical_features= [0])
x = oneHtEnc_x.fit_transform(x).toarray()


lblEnc_y = LabelEncoder()

y = lblEnc_y.fit_transform(y)

z = oneHtEnc_x.inverse_transform(x[:, 0:3])

a = lblEnc_x.inverse_transform(z.astype(int))

# splitting datasets into Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)













