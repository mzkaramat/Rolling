# importing libaries ----
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

data = pd.read_csv("result.csv")

data.head()

data[['temperature','humidity']].head()

data = data[['temperature','humidity']]

data.head()

X_train = pd.DataFrame(data, columns = ['temperature', 'humidity'])

X_train.head()

X_train.columns = ['x1', 'x2']

# training the model
clf = IsolationForest(max_samples=100, random_state=123)
clf.fit(X_train)

X_outliers = pd.DataFrame([{'x1':10,'x2':69.79},{'x1':27,'x2':69.79}])

import pickle

#
# Create your model here (same as above)
#

# Save to file in the current working directory
pkl_filename = "anom.pkl"  
with open(pkl_filename, 'wb') as file:  
    pickle.dump(clf, file)