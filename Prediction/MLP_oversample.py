import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, f1_score, matthews_corrcoef
from tqdm import tqdm
import joblib
import os

# 设置你的CSV文件路径
file_path = '.\\airport_weather_2020.csv'
df = pd.read_csv(file_path)
print("Initial DataFrame shape:", df.shape)

df.loc[df['CANCELLED'] == 1 , 'DEP_DELAY'] = 999
df.loc[df['CANCELLED'] == 1 , 'DEP_TIME'] = '00:00:00 AM'

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
df.loc[df['CANCELLED'] == 1 , 'DEP_HOUR'] = '24'
df.drop('DEP_TIME', axis=1, inplace=True)
df.drop('CANCELLED', axis=1, inplace=True)
df.reset_index(drop=True, inplace=True)

# 独热编码
encoder = OneHotEncoder(sparse_output=False)
columns_to_encode = ['DAY_OF_WEEK', 'DEP_HOUR', 'MONTH']
encoded_data = encoder.fit_transform(df[columns_to_encode])
encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(columns_to_encode))
df = pd.concat([df, encoded_df], axis=1)
df.drop(columns_to_encode, axis=1, inplace=True)

# 分类延迟时间
def categorize_delay(delay):
    if delay < 0:
        return 0
    elif 0 <= delay < 10:
        return 1
    elif 10 <= delay < 20:
        return 2
    elif 20 <= delay < 30:
        return 3
    else:
        return 4

def categorize_delay_biary(delay):
    if delay <= 15:
        return 0
    else:
        return 1

df['DEP_DELAY_Category'] = df['DEP_DELAY'].apply(categorize_delay_biary)

# 划分数据集
X = df.drop(['DEP_DELAY_Category', 'DEP_DELAY'], axis=1)
y = df['DEP_DELAY_Category']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
class_set = np.unique(y)

# 训练模型
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

oversampler = RandomOverSampler(random_state=42)
X_resampled, y_resampled = oversampler.fit_resample(X_train_scaled, y_train)

epochs = 5  # 定义迭代次数
batch_size = 256  # 批量大小
hidden_layer_size = (50, 50,)
learning_rate = 0.001
shuffle = True

# 创建 MLP 模型
mlp = MLPClassifier(hidden_layer_sizes=hidden_layer_size, batch_size=batch_size, learning_rate_init=learning_rate, max_iter=1, shuffle=shuffle, verbose=True, warm_start=True, random_state=42)

with tqdm(total=epochs, desc=f'Processing', unit='iteration') as pbar:
    for epoch in range(epochs):
        mlp.partial_fit(X_resampled, y_resampled, classes=class_set)
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
encoder_path = os.path.join(output_dir, 'mlp_os_cls_encoder.joblib')
scaler_path = os.path.join(output_dir, 'mlp_os_cls_scaler.joblib')
model_path = os.path.join(output_dir, 'mlp_os_cls.joblib')
joblib.dump(encoder, encoder_dir)
joblib.dump(scaler, scaler_dir)
joblib.dump(mlp, model_dir)
