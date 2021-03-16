# Data preprocessing

# Import the libraries.
import numpy as np
import matplotlib .pyplot as plt
import pandas as pd

# importing the datasets.
datasets = pd.read_csv('D:\\04_GIT_Repos\\PythonProjects\\MachineLearningCourse\\Part 1 - Data Preprocessing\\Data.csv')

X = datasets.iloc[:, :-1].values
y = datasets.iloc[:, 3].values

# Taking care of the missing data of the datasets.
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(missing_values = np.nan, strategy = 'mean')
imputer = imputer.fit(X[:, 1:3])
X[:, 1:3] = imputer.transform(X[:, 1:3])

# Encoding categorical data

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer

ct = ColumnTransformer([('encoder', OneHotEncoder(), [0])], remainder='passthrough')
X = np.array(ct.fit_transform(X), dtype=np.float)
X[:, 3:X.size] = imputer.transform(datasets.iloc[:, 1:3])
labelEncoder_y = LabelEncoder()
y = labelEncoder_y.fit_transform(y)

#splitting the dataset into the training set and Test set.
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Feature scaling
from sklearn.preprocessing import StandardScaler

sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)


