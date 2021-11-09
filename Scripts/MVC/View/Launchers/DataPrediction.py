from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np

DATASETS_PATH = 'D:\Projects\PYTHON\PacmanByMobik\Datasets'


data = pd.read_csv(DATASETS_PATH + '\GameStatistic.csv')
# print(data.shape)
print(data.head())


x_train, x_test, y_train, y_test = train_test_split(data.median_income,
                                                    data.median_house_value,
                                                    test_size = 0.2)
regr = LinearRegression()
preds = regr.predict(np.array(x_test).reshape(-1,1))