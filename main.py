import pandas as pd
import numpy as np
import joblib
import util as util
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

dataset = pd.read_csv('data/shorterurls_test1.csv')

# split into input (X) and output (Y) variables
X = dataset.iloc[:, 0:46].values
y = dataset.iloc[:, 46].values

# split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=0)

# scale values
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
# construct model
regressor = RandomForestClassifier(n_estimators=50, random_state=10, verbose=1)
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)
# print results
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
print(accuracy_score(y_test, y_pred))

modelsave = input('Save this model? Y/N')

if modelsave == "Y" or modelsave == "y":
    # save model as pickle file
    filename = "model/rf_model.joblib"
    joblib.dump(regressor, filename)
else:
    print('Done')
