import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, f1_score, matthews_corrcoef
from tqdm import tqdm
import joblib
import os


random_seed = 23333
test_split = 0.2
epochs = 10
batch_size = 256
hidden_layer_size = (50, 50, 30)


def data_etl(file_path):
    df = pd.read_csv(file_path)
    print("Initial DataFrame shape:", df.shape)

    # drop columns
    columns_to_drop = ['YEAR', 'FL_DATE', 'ORIGIN', 'ORIGIN_CITY_NAME', 'ORIGIN_STATE_NM', 'DEST', 'DEST_CITY_NAME',
                       'DEST_STATE_NM', 'STATION',
                       'DATE', 'NAME', 'FRSHTT', 'WBAN_ID', 'CALL_SIGN']
    columns_to_drop_unavailable = ['DEWP', 'WDSP', 'MXSPD', 'PRCP', 'SNDP', ]
    df.drop(columns_to_drop, axis=1, inplace=True)
    df.drop(columns_to_drop_unavailable, axis=1, inplace=True)
    print("DataFrame after dropping columns:", df.shape)

    # deal with cancelled flights
    cancelled_count = len(df[df['CANCELLED'] == 1])
    not_cancelled_rows = df[df['CANCELLED'] == 0]
    # random sampling follow the distribution of not_cancelled_rows
    sampled_values = not_cancelled_rows['DEP_TIME'].sample(n=cancelled_count, replace=True,
                                                           random_state=random_seed).tolist()
    df.loc[df['CANCELLED'] == 1, 'DEP_TIME'] = sampled_values
    df.loc[df['CANCELLED'] == 1, 'DEP_DELAY'] = 999
    df.drop('CANCELLED', axis=1, inplace=True)

    # 删除缺失值
    df.dropna(inplace=True)
    df = df.sample(frac=0.4, random_state=random_seed)
    print("DataFrame after dropping NA:", df.shape)

    # 将小时转换为时间
    df['DEP_HOUR'] = df['DEP_TIME'].str[:2]
    df.loc[df['DEP_HOUR'] == '24', 'DEP_HOUR'] = '00'
    df.drop('DEP_TIME', axis=1, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


df_2020 = data_etl('.\\airport_weather_2020.csv')
df_2021 = data_etl('.\\airport_weather_2021.csv')
df_2022 = data_etl('.\\airport_weather_2022.csv')
df = pd.concat([df_2020, df_2021, df_2022], ignore_index=True)

# 独热编码
encoder = OneHotEncoder(sparse_output=False)
columns_to_encode = ['DAY_OF_WEEK', 'DEP_HOUR', 'MONTH']
encoded_data = encoder.fit_transform(df[columns_to_encode])
df.drop(columns_to_encode, axis=1, inplace=True)
encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(columns_to_encode))
df = pd.concat([df, encoded_df], axis=1)


def categorize_VISIB(visib):
    if visib < 4:
        return 0
    elif visib <= 10:
        return 1
    else:
        return 2


def categorize_delay_biary(delay):
    if delay <= 15:
        return 0
    else:
        return 1


df['VISIB'] = df['VISIB'].apply(categorize_VISIB)
df['DEP_DELAY_Category'] = df['DEP_DELAY'].apply(categorize_delay_biary)

# 划分数据集
X = df.drop(['DEP_DELAY_Category', 'DEP_DELAY'], axis=1)
y = df['DEP_DELAY_Category']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_split, random_state=random_seed)
class_set = np.unique(y)

# 训练模型
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 创建 MLP 模型
mlp = MLPClassifier(hidden_layer_sizes=hidden_layer_size, batch_size=batch_size, max_iter=1, warm_start=True, random_state=random_seed)
with tqdm(total=epochs, desc=f'Processing', unit='iteration') as pbar:
    for epoch in range(epochs):
        mlp.partial_fit(X_train_scaled, y_train, classes=class_set)
        pbar.update(1)

# 进行预测
y_pred = mlp.predict(X_test_scaled)
# 评估模型
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average='weighted')
# 计算 Matthews 相关系数
mcc = matthews_corrcoef(y_test, y_pred)
print("Accuracy:", accuracy)
print("F1 Score:", f1)
print(f"Matthews Correlation Coefficient: {mcc}")
print("\nClassification Report:\n", classification_report(y_test, y_pred))

output_dir = '.'
encoder_path = os.path.join(output_dir, 'mlp_cls_encoder.joblib')
scaler_path = os.path.join(output_dir, 'mlp_cls_scaler.joblib')
model_path = os.path.join(output_dir, 'mlp_cls.joblib')
joblib.dump(encoder, encoder_path)
joblib.dump(scaler, scaler_path)
joblib.dump(mlp, model_path)
