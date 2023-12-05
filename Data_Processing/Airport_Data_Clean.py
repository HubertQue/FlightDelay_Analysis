import pandas as pd

def convert_time(t):
    if pd.isna(t):
        return None
    t = int(t)
    hour = t // 100  
    minute = t % 100  
    return f"{hour:02d}:{minute:02d}" 


def data_clean(filename):
    df = pd.read_csv(filename)
    
#   drop unnecessary attribute
    df = df.drop('MONTH', axis=1)
    df = df.drop('DAY_OF_MONTH', axis=1)
    df = df.drop('TAIL_NUM', axis=1)
    df = df.drop('OP_CARRIER_FL_NUM', axis=1)
    df = df.drop('ORIGIN_AIRPORT_ID', axis=1)
    df = df.drop('ORIGIN_STATE_ABR', axis=1)
    df = df.drop('DEST_AIRPORT_ID', axis=1)
    df = df.drop('DEST_STATE_ABR', axis=1)
    df = df.drop('DEP_DELAY_NEW', axis=1)
    df = df.drop('DEP_DEL15', axis=1)
    df = df.drop('ARR_TIME', axis=1)
    df = df.drop('ARR_DELAY', axis=1)
    df = df.drop('ARR_DELAY_NEW', axis=1)
    df = df.drop('ARR_DEL15', axis=1)
    df = df.drop('AIR_TIME', axis=1)
    df = df.drop('FLIGHTS', axis=1)
    df = df.drop('DISTANCE', axis=1)
    df = df.drop('CARRIER_DELAY', axis=1)
    df = df.drop('WEATHER_DELAY', axis=1)
    df = df.drop('NAS_DELAY', axis=1)
    df = df.drop('SECURITY_DELAY', axis=1)
    df = df.drop('LATE_AIRCRAFT_DELAY', axis=1)
    
    df['FL_DATE'] = pd.to_datetime(df['FL_DATE'])
    df['FL_DATE'] = df['FL_DATE'].dt.strftime('%Y-%m-%d')

    df['DEP_TIME'] = df['DEP_TIME'].apply(convert_time)
    
    df.to_csv('../../data/airport-2022-cleaned.csv', index=False)


airport_csv = '../../data/airport-2022.csv'
data_clean(airport_csv)
