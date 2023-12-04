import pandas as pd
import joblib

def get_importance(model_path=''):
    model_loaded = joblib.load(model_path)
    # get importance
    importance = model_loaded.feature_importances_
    # summarize feature importance
    aggregated_importance = {}
    for i,v in enumerate(importance):
        print('Feature: %0d, %s, Importance Score: %.3f' % (i, feature_names[i],v))
        aggregated_importance[aggregated_feature_names[i]] = aggregated_importance.get(aggregated_feature_names[i], 0) + v
    for f, imp in aggregated_importance.items():
        print('Aggregated Feature: %s, Importance Score: %.3f' % (f, imp))

feature_names = ['ELEVATION', 'TEMP', 'DEWP', 'VISIB', 'WDSP', 'MXSPD', 'MAX', 'MIN', 'PRCP', 'SNDP', 'Fog', 'Rain or Drizzle', 'Snow or Ice Pellets', 'Hail', 'Thunder', 'Tornado or Funnel Cloud', 'DAY_OF_WEEK_1', 'DAY_OF_WEEK_2', 'DAY_OF_WEEK_3', 'DAY_OF_WEEK_4', 'DAY_OF_WEEK_5', 'DAY_OF_WEEK_6', 'DAY_OF_WEEK_7', 'DEP_HOUR_00', 'DEP_HOUR_01', 'DEP_HOUR_02', 'DEP_HOUR_03', 'DEP_HOUR_04', 'DEP_HOUR_05', 'DEP_HOUR_06', 'DEP_HOUR_07', 'DEP_HOUR_08', 'DEP_HOUR_09', 'DEP_HOUR_10', 'DEP_HOUR_11', 'DEP_HOUR_12', 'DEP_HOUR_13', 'DEP_HOUR_14', 'DEP_HOUR_15', 'DEP_HOUR_16', 'DEP_HOUR_17', 'DEP_HOUR_18', 'DEP_HOUR_19', 'DEP_HOUR_20', 'DEP_HOUR_21', 'DEP_HOUR_22', 'DEP_HOUR_23', 'DEP_HOUR_24', 'MONTH_1', 'MONTH_2', 'MONTH_3', 'MONTH_4', 'MONTH_5', 'MONTH_6', 'MONTH_7', 'MONTH_8', 'MONTH_9', 'MONTH_10', 'MONTH_11', 'MONTH_12']
aggregated_feature_names = ['ELEVATION', 'TEMP', 'DEWP', 'VISIB', 'WDSP', 'MXSPD', 'MAX', 'MIN', 'PRCP', 'SNDP', 'Fog', 'Rain or Drizzle', 'Snow or Ice Pellets', 'Hail', 'Thunder', 'Tornado or Funnel Cloud', 'DAY_OF_WEEK', 'DAY_OF_WEEK', 'DAY_OF_WEEK', 'DAY_OF_WEEK', 'DAY_OF_WEEK', 'DAY_OF_WEEK', 'DAY_OF_WEEK', 'DEP_HOUR', 'DEP_HOUR', 'DEP_HOUR', 'DEP_HOUR', 'DEP_HOUR', 'DEP_HOUR', 'DEP_HOUR', 'DEP_HOUR', 'DEP_HOUR', 'DEP_HOUR', 'DEP_HOUR', 'DEP_HOUR', 'DEP_HOUR', 'DEP_HOUR', 'DEP_HOUR', 'DEP_HOUR', 'DEP_HOUR', 'DEP_HOUR', 'DEP_HOUR', 'DEP_HOUR', 'DEP_HOUR', 'DEP_HOUR', 'DEP_HOUR', 'DEP_HOUR', 'DEP_HOUR', 'MONTH', 'MONTH', 'MONTH', 'MONTH', 'MONTH', 'MONTH', 'MONTH', 'MONTH', 'MONTH', 'MONTH', 'MONTH', 'MONTH']

if __name__ == '__main__':
    model_path = '.\\rf_cls.joblib'
    get_importance(model_path=model_path)
