import pickle
# importing libaries ----
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import datetime

pkl_filename = "anom.pkl"  
# Load from file
with open(pkl_filename, 'rb') as file:  
    pickle_model = pickle.load(file)

X_outliers = pd.DataFrame([{'x1':10,'x2':69.79}])
y_pred_outliers = pickle_model.predict(X_outliers)
if y_pred_outliers[0] == -1:
    print("Anom")
else:
    print("Nothing to worry about")