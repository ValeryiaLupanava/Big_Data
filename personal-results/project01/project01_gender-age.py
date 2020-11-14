#!/opt/anaconda/envs/bd9/bin/python


#import time

#t0 = time.clock()

import sys
import pandas as pd
import numpy as np
import re
import json
#import pickle
from urllib.parse import urlparse
from urllib.request import urlretrieve, unquote
from pandas.io.json import json_normalize
import datetime
#from sklearn import preprocessing
import pickle


# функция для выделения domain из url
def url2domain(url):
    url = re.sub('(http(s)*://)+', 'http://', url)
    parsed_url = urlparse(unquote(url.strip()))
    if parsed_url.scheme not in ['http','https']: return None
    netloc = re.search("(?:www\.)?(.*)", parsed_url.netloc).group(1)
    if netloc is not None: return str(netloc.encode('utf8')).strip()
    return None


# фукнция конвертации timestamp в datetime
def datetime_conv(value):
    return datetime.datetime.fromtimestamp(value / 1e3)

# загражем данные из стандартного входа
columns=['gender','age','uid','user_json']
df = pd.read_table(sys.stdin, sep='\t', header=None, names=columns)

#file_path = '/data/share/project01/gender_age_dataset.txt'
#df = pd.read_csv(file_path, sep='\t')

# выбираем данные с неизвестными таргетами
df = df[((df.gender == '-') & (df.age == '-'))]

# удаляем столбцы с таргетами
df.drop(labels=['gender','age'],axis=1, inplace=True)

# обновляем индексы
df.reset_index(drop=True, inplace=True)

# убираем лишний уровень дикта в столбце user_json
df['user_json'] = json_normalize(df['user_json'].apply(json.loads))

# конвертируем данные в дикт
df2_dict = df.to_dict('records')

# разбиваем на кусочки всё, что есть
df2_norm = pd.DataFrame(json_normalize(df2_dict, 'user_json', ['uid']),columns=['uid','timestamp','url'])

# выделяем домейны
df2_norm['domain'] = df2_norm['url'].apply(url2domain)

# конвертируем timestamp в даты
df2_norm['datetime'] = df2_norm['timestamp'].apply(datetime_conv)
df2_norm['datetime'] = pd.to_datetime(df2_norm['datetime'], format='%Y%m%d%h%')
df3 = df2_norm.drop(labels=['url','timestamp'],axis=1)

# создаём столбцы с временем
df3['hour'] = df3['datetime'].dt.hour
df3['day'] = df3['datetime'].dt.day
df3['month'] = df3['datetime'].dt.month

# категоризируем даты
df3['day_part'] = 'Unknown'
df3.loc[df3['hour'].between(6, 12, inclusive=True), 'day_part'] = 'Morning'
df3.loc[df3['hour'].between(13, 18, inclusive=True), 'day_part'] = 'Afternoon'
df3.loc[df3['hour'].between(19, 24, inclusive=True), 'day_part'] = 'Evening'
df3.loc[df3['hour'].between(0, 5, inclusive=True), 'day_part'] = 'Night'

# категоризируем даты
df3['season'] = 'Unknown'
df3.loc[df3['month'].between(3, 5, inclusive=True), 'season'] = 'Spring'
df3.loc[df3['month'].between(6, 8, inclusive=True), 'season'] = 'Summer'
df3.loc[df3['month'].between(9, 11, inclusive=True), 'season'] = 'Autumn'
df3.loc[df3['month'].between(1, 2, inclusive=True), 'season'] = 'Winter'
df3.loc[df3['month'].between(12, 12, inclusive=True), 'season'] = 'Winter'

# категоризируем даты
df3['week_day'] = df3['datetime'].dt.day_name()
workdays = ['Wednesday', 'Thursday', 'Friday', 'Monday', 'Tuesday']
weekend = ['Saturday', 'Sunday']

# категоризируем даты
df3['day_type'] = df3['week_day'].isin(workdays)
df3['day_type'] = df3['day_type'].replace([True, False], ['Workday', 'Weekend'])

# удаляем одинаковые строки в датасете
df4 = df3.drop_duplicates(subset=['uid','domain','day_part', 'season', 'week_day', 'day_type'], keep='first')

# удаляем лишние столбцы с датами
df4.drop(labels=['datetime','hour','day','month'],axis=1, inplace=True)

# сбрасываем индексы
df4.reset_index(drop=True, inplace=True)

# загружаем таблицу со статистикой по сайтам
sex_age_csv = 'project01/sex_age_stat.csv'
sex_age_stat = pd.read_csv(sex_age_csv, sep='\t')

# генерируем на её основе новые фичи в датасете
df5_test = pd.merge(df4, sex_age_stat, on=['domain', 'domain'], how='left')

# заполняем пустые строки средними значениями по столбцам
for i in ['F', 'M', '18-24', '25-34', '35-44', '45-54', '>=55']:
    df5_test[i].fillna(df5_test[i].mean(), inplace=True)

# удаляем столбец domain
df5_test.drop(labels='domain',axis=1, inplace=True)

# загружаем модели энкодеров
m_le_day_part = "project01/le_day_part.pickle"
m_le_season   = "project01/le_season  .pickle"
m_le_week_day = "project01/le_week_day.pickle"
m_le_day_type = "project01/le_day_type.pickle"
m_le_gender   = "project01/le_gender  .pickle"
m_le_age      = "project01/le_age     .pickle"

le_day_part = pickle.load(open(m_le_day_part, 'rb'))
le_season   = pickle.load(open(m_le_season  , 'rb'))
le_week_day = pickle.load(open(m_le_week_day, 'rb'))
le_day_type = pickle.load(open(m_le_day_type, 'rb'))
le_gender   = pickle.load(open(m_le_gender  , 'rb'))
le_age      = pickle.load(open(m_le_age     , 'rb'))

# шифруем категории в датасете
df5_test['day_part'] = le_day_part.transform(df5_test['day_part'].astype(str))
df5_test['season']   = le_season  .transform(df5_test['season'].astype(str))
df5_test['week_day'] = le_week_day.transform(df5_test['week_day'].astype(str))
df5_test['day_type'] = le_day_type.transform(df5_test['day_type'].astype(str))

# удаляем uid 
x = np.array(df5_test.drop(labels='uid',axis=1))

# загружаем модели предсказания
model_file_1 = "project01/project01_model_gender.pickle"
model_file_2 = "project01/project01_model_age.pickle"

# делаем предсказания
p1 = pickle.load(open(model_file_1, 'rb'))
p2 = pickle.load(open(model_file_2, 'rb'))

# формируем таблицу с результатами
uid = np.array(df5_test['uid']).reshape(-1,1)
gender = p1.predict_proba(x)[:,1].reshape(-1,1)
age = p2.predict(x).reshape(-1,1)
result = pd.DataFrame(np.hstack([uid,gender,age]), columns=['uid', 'gender','age'])

result['gender'] = result['gender'].map(lambda item : '-' if item < 0.55 and item > 0.45 else round(item))

# конвертируем результаты в int
#result['gender'] = result['gender'].astype(int)
result['age'] = result['age'].astype(int)

# удаляем строки с одинаковыми uid и оставляем для каждого uid значения, наиболее часто встречающиеся
result_fin = result.groupby('uid').agg(lambda x:x.value_counts().index[0]).reset_index(drop=False)

# возвращаем обратно лэйблы по энкодерам
result_fin['gender'] = result_fin['gender'].replace(0, 'F')
result_fin['gender'] = result_fin['gender'].replace(1, 'M')
#result_fin['gender'] = le_gender.inverse_transform(result_fin['gender'])
result_fin['age'] = le_age.inverse_transform(result_fin['age'])

# сортируем результат по возрастанию
output = result_fin
output.sort_values(by='uid',axis = 0, ascending = True, inplace = True)

#output['gender'].value_counts(dropna = False)
#output['age'].value_counts(dropna = False)
#t1 = time.clock() - t0
#print("Time elapsed: ", t1) # CPU seconds elapsed (floating point)
#print("SLA: ", t1/output.shape[0])

# передаём результаты на выход в виде json
sys.stdout.write(output.to_json(orient='records'))