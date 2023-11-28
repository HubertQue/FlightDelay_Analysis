import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

# 设置你的CSV文件路径
file_path = 'data/airport_weather_2020.csv'  # 修改为你的文件路径
df = pd.read_csv(file_path)
print("Initial DataFrame shape:", df.shape)

# 删除不需要的列
columns_to_drop = ['YEAR', 'FL_DATE', 'ORIGIN', 'ORIGIN_CITY_NAME', 'ORIGIN_STATE_NM', 'DEST', 'DEST_CITY_NAME', 'DEST_STATE_NM', 'CANCELLED', 'STATION',
                   'DATE', 'NAME', 'FRSHTT', 'WBAN_ID', 'CALL_SIGN']
df.drop(columns_to_drop, axis=1, inplace=True)
print("DataFrame after dropping columns:", df.shape)

# 删除缺失值
df.dropna(inplace=True)
print("DataFrame after dropping NA:", df.shape)

# 将小时转换为时间
df['DEP_HOUR'] = df['DEP_TIME'].str[:2]
df.drop('DEP_TIME', axis=1, inplace=True)
df.reset_index(drop=True, inplace=True)

# 独热编码
encoder = OneHotEncoder(sparse=False)
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

df['DEP_DELAY_Category'] = df['DEP_DELAY'].apply(categorize_delay)

# 划分数据集
X = df.drop(['DEP_DELAY_Category', 'DEP_DELAY'], axis=1)
y = df['DEP_DELAY_Category']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 训练SVM模型
svm_classifier = SVC(random_state=42)
svm_classifier.fit(X_train, y_train)

# 进行预测
y_pred_svm = svm_classifier.predict(X_test)

# 评估模型
accuracy_svm = accuracy_score(y_test, y_pred_svm)
f1_svm = f1_score(y_test, y_pred_svm, average='weighted')
print("SVM Accuracy:", accuracy_svm)
print("SVM F1 Score:", f1_svm)
print("\nSVM Classification Report:\n", classification_report(y_test, y_pred_svm))