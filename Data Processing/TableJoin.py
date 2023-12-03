#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


df_airport = pd.read_csv('../data/airport-2020-cleaned.csv')
df_airport.head(3)


# In[3]:


df_weather = pd.read_csv('../data/weather_2020.csv')
df_weather.head(3)


# In[4]:


df_code = pd.read_csv('../data/id_mapping.csv', dtype={'WBAN_ID': str})
df_code.head(15)


# In[5]:


df_weather['STATION'] = df_weather['STATION'].astype(str).str[-5:]
df_weather.head(3)


# In[6]:


weather_code_df = pd.merge(df_weather, df_code, left_on='STATION', right_on='WBAN_ID', how='inner')


# In[7]:


weather_code_df.shape


# In[8]:


weather_code_df.head()


# In[ ]:





# In[9]:


weather_code_df['DATE'] = pd.to_datetime(weather_code_df['DATE'])
weather_code_df['MONTH'] = weather_code_df['DATE'].dt.month
weather_code_df['DATE'] = weather_code_df['DATE'].dt.strftime('%Y-%m-%d')
weather_code_df.head()


# In[10]:


df_airport.head()


# In[11]:


final_df = pd.merge(
    df_airport,
    weather_code_df,
    how='inner',
    left_on=['ORIGIN', 'FL_DATE'],
    right_on=['CALL_SIGN', 'DATE']
)


# In[12]:


final_df.shape


# In[13]:


final_df.head()


# In[14]:


df = final_df


# In[15]:


df


# In[16]:


df.columns


# In[17]:


final_df.to_csv('../data/airport_weather_2020.csv', index=False)


# In[18]:


pearson_corr = final_df.corr(method='pearson')['DEP_DELAY'].sort_values(ascending=False)


# In[19]:


pearson_corr


# In[20]:


final_df = final_df.dropna()


# In[21]:


pearson_corr = final_df.corr(method='pearson')['DEP_DELAY'].sort_values(ascending=False)
pearson_corr


# In[22]:


corr = final_df.corr()['DEP_DELAY'].sort_values(ascending=False)


# In[23]:


corr


# In[24]:


final_df.tail()


# In[ ]:




