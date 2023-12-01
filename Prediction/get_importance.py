import pandas as pd
import joblib

def get_importance(file_path=''):
    model_loaded = joblib.load(model_path)
    # get importance
    importance = model_loaded.feature_importances_
    # summarize feature importance
    for i,v in enumerate(importance):
        print('Feature: %0d, Importance Score: %.3f' % (i,v))

# feature_names = iris.feature_names
# feature_importance_dict = dict(zip(feature_names, feature_importances))
#for feature, importance in feature_importance_dict.items():
#    print(f"{feature}: {importance}")

if __name__ == '__main__':
    file_path = ''
    get_importance(file_path=file_path)
