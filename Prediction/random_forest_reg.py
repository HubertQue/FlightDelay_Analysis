import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import os

# 设置你的CSV文件路径
file_path = '.\\airport_weather_2020.csv'
df = pd.read_csv(file_path)
print("Initial DataFrame shape:", df.shape)

df.loc[df['CANCELLED'] == 1 , 'DEP_DELAY'] = 999
# df.loc[df['CANCELLED'] == 1 , 'DEP_TIME'] = '00:00:00 AM'

# 删除不需要的列
columns_to_drop = ['YEAR', 'FL_DATE', 'ORIGIN', 'ORIGIN_CITY_NAME', 'ORIGIN_STATE_NM', 'DEST', 'DEST_CITY_NAME', 'DEST_STATE_NM', 'STATION',
                   'DATE', 'NAME', 'FRSHTT', 'WBAN_ID', 'CALL_SIGN']
df.drop(columns_to_drop, axis=1, inplace=True)
print("DataFrame after dropping columns:", df.shape)

# 删除缺失值
df.dropna(inplace=True)
print("DataFrame after dropping NA:", df.shape)

# 将小时转换为时间
df['DEP_HOUR'] = df['DEP_TIME'].str[:2]
df.loc[df['DEP_HOUR'] == '24' , 'DEP_HOUR'] = '00'
# df.loc[df['CANCELLED'] == 1 , 'DEP_HOUR'] = '24'
df.drop('DEP_TIME', axis=1, inplace=True)
df.drop('CANCELLED', axis=1, inplace=True)
df.reset_index(drop=True, inplace=True)

#print(df.head())

# 独热编码
encoder = OneHotEncoder(sparse_output=False)
columns_to_encode = ['DAY_OF_WEEK', 'DEP_HOUR', 'MONTH']
encoded_data = encoder.fit_transform(df[columns_to_encode])
encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(columns_to_encode))
df = pd.concat([df, encoded_df], axis=1)
df.drop(columns_to_encode, axis=1, inplace=True)

#print(df.head())
print(df.columns.tolist())

# 划分数据集
X = df.drop(['DEP_DELAY'], axis=1)
y = df['DEP_DELAY']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 训练随机森林模型
rf_regressor = RandomForestRegressor(n_estimators=30, random_state=42)
rf_regressor.fit(X_train, y_train)

# 进行预测
y_pred = rf_regressor.predict(X_test)

# 评价
mse = mean_squared_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred, squared=False)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'Mean Squared Error (MSE): {mse}')
print(f'Root Mean Squared Error (RMSE): {rmse}')
print(f'Mean Absolute Error (MAE): {mae}')
print(f'R-squared (R2): {r2}')

output_dir = '.'
encoder_path = os.path.join(output_dir, 'rf_reg_encoder.joblib')
model_path = os.path.join(output_dir, 'rf_reg.joblib')
joblib.dump(encoder, encoder_path)
joblib.dump(rf_regressor, model_path)
