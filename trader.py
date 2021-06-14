import argparse
from fbprophet import Prophet
import pandas as pd
from matplotlib import pyplot

parser = argparse.ArgumentParser()
parser.add_argument('--training', 
                        default='training.csv',
                        help='PATH TO YOUR ELECTRICITY DATA(.csv)')
parser.add_argument('--testing', 
                        default='testing.csv',
                        help='PATH TO YOUR ELECTRICITY DATA(.csv)')
parser.add_argument('--output', 
                        default='output.csv',
                        help='OUTPUT FILE NAME(.csv)')
args = parser.parse_args()


# load data and concat
train_trade_df = pd.read_csv(args.training, names=['y', 'high', 'low', 'close'])
test_trade_df = pd.read_csv(args.testing, names=['y', 'high', 'low', 'close'])
trade_size = (train_trade_df.size + test_trade_df.size) // 4

ds = pd.Series(pd.date_range('1/1/2017', freq='D', periods=trade_size)).to_frame(name='ds')
df = pd.concat([train_trade_df, test_trade_df], ignore_index=True)
df = pd.concat([ds, df], axis=1)


# normalization
columns_name = ['y', 'high', 'low', 'close']
for column in columns_name:
    df[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min())



if_hold = False
price = 0.0
action = []

# train and predict
for i in range(train_trade_df.size//4, trade_size-1):
    df_train = df.loc[df["ds"]<=df['ds'][i]]
    df_test = df.loc[df["ds"]==df['ds'][i+1]]

    model = Prophet(changepoints=[df['ds'][i]])
    model.add_regressor('high')
    model.add_regressor('low')
    model.add_regressor('close')
    model.fit(df_train)

    pred = model.predict(df_test.drop(columns='y'))
    output = pred[['ds', 'yhat']]
    if if_hold == False:
        if output['yhat'].values[0] < df['y'][i]:
            price = df['y'][i+1]
            if_hold = True
            action.append(1)
        else:
            action.append(0)
    else:
        if output['yhat'].values[0] < price:
            if_hold = False
            action.append(-1)
        else:
            action.append(0)

# output
result = pd.DataFrame(action)
result.to_csv(args.output, index=False, header=False)