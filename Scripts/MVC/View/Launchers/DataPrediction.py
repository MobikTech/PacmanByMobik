import numpy
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

DATASETS_PATH = 'D:\Projects\PYTHON\PacmanByMobik\Datasets'


class AttributeConverter():

    @staticmethod
    def denormalize_status(value):
       if value in [0, '0']:
           return 'lose'
       else:
           return 'win'

    @staticmethod
    def denormalize_algorithm(value):
       if value in [0, '0']:
           return 'Minimax'
       else:
           return 'Expectimax'

class ATTRIBUTES():
    STATUS = 1,
    SCORE = 2,
    TIME = 3,
    ALGORITHM = 4,
    CROSSROADS_COUNT = 5


def normalize(df):
    statusList = df['Status'].tolist()
    algorithmList = df['Algorithm'].tolist()

    labelEncoderStatus = LabelEncoder()
    labelEncoderStatus.fit(statusList)
    labelsStatus = labelEncoderStatus.transform(statusList)
    df['Status'] = pd.Series(labelsStatus)

    labelEncoderAlgorithm = LabelEncoder()
    labelEncoderAlgorithm.fit(algorithmList)
    labelsAlgorithm = labelEncoderAlgorithm.transform(algorithmList)
    df['Algorithm'] = pd.Series(labelsAlgorithm)

    return df

def correctDataFrame(df: pd.DataFrame):
    print(df)
    crossroadsValues = list()
    for crossroadListValue in df['CrossroadsCount']:
        crossroadsValues.append(crossroadListValue[0])
    df['CrossroadsCount'] = crossroadsValues
    convert_dict = {'Status': int,
                    'Score': int,
                    'Time': float,
                    'Algorithm': int,
                    'CrossroadsCount': int
                    }
    df = df.astype(convert_dict)
    return df

def denormalize(df):
    statusValues = df['Status']
    AlgorithmValues = df['Algorithm']

    newStatusValues = list()
    newAlgValues = list()
    for status in statusValues:
        newStatusValues.append(AttributeConverter.denormalize_status(status))
    for algValue in AlgorithmValues:
        newAlgValues.append(AttributeConverter.denormalize_algorithm(algValue))

    df['Status'] = newStatusValues
    df['Algorithm'] = newAlgValues

    return df


df = pd.read_csv(DATASETS_PATH + '\GameStatistic.csv')
df = normalize(df)

x = np.array(df[['CrossroadsCount']])
y = np.array(df[['Status', 'Score', 'Time', 'Algorithm']])

newCrossroadsValues = [[70], [80], [90], [100], [110], [120]]
model = LinearRegression()
model.fit(x, y)
prediction = pd.DataFrame(model.predict(newCrossroadsValues), columns=['Status', 'Score', 'Time', 'Algorithm'])
prediction['CrossroadsCount'] = newCrossroadsValues

prediction = correctDataFrame(prediction)
print(prediction.dtypes)
final_df = df.append(prediction)
final_df = denormalize(final_df)

final_df.to_csv(DATASETS_PATH + '\PredictedStatistic.csv', index=False)
print(final_df)


