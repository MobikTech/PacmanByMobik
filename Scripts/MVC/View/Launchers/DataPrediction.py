from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np

DATASETS_PATH = 'D:\Projects\PYTHON\PacmanByMobik\Datasets'


data = pd.read_csv(DATASETS_PATH + '\GameStatistic.csv')
# print(data.shape)
print(data)
print(data.at[0, 'Score'])

x = np.array(data[['CrossroadsCount']])
y = np.array(data['Status', 'Score', 'Time', 'Algorithm'])
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)

model = LinearRegression()
preds = model.predict(np.array(x_test).reshape(-1,1))