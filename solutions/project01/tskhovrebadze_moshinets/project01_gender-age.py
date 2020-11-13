#!/opt/anaconda/envs/bd9/bin/python

import numpy as np
import pandas as pd
import os, sys
import pickle
import xgboost
from urllib.parse import urlparse, unquote
import json
import pickle
import re

#В процессе отладки этапы писались в лог-файл. Перед финальной проверкой это было отключено чтобы случайно не поймать ошибку записи в файл
#file = open('/data/home/ruslan.tskhovrebadze/log.txt', 'w')

def ts2dwt(ts):
    try:
        ts = ts / 1000
        dw = datetime.utcfromtimestamp(ts).weekday()
        t = datetime.utcfromtimestamp(ts).strftime('%H')
        return str(dw) + '_' + t
    except:
        return


def url2domain(url):
    try:
        #file.write('Entered url2domain function')
        url = re.sub(r'https?://https?://', 'http://', str.lower(url))
        a = urlparse(unquote(url.strip()))
        if (a.scheme in ['http','https']):
            b = re.search("(?:www\.)?(.*)",a.netloc).group(1)
            if b is not None:
                return str(b).strip()
            else:
                return ''
        else:
            return ''
    except Exception as e:
        #file.write("Exception inside url2domain: {0} \n".format(str(e)))
        return
      
def data_prep(x):
    try:
        data = []
        visits = json.loads(x)
        for i in range(len(visits['visits'])):
            sj = url2domain(visits['visits'][i]['url'])
            #file.write('url2domain input  was {0}'.format(str(visits['visits'][i]['url'])))  
            #file.write('Result is {0}'.format(str(sj)))
            data.append(sj)
        return data
    except Exception as e:
        #file.write("Exception inside function: {0} \n".format(str(e)))
        return
      
try:         
    columns=['gender','age','uid','user_json']

    gen_test_df = pd.read_table(
        sys.stdin, 
        sep='\t', 
        header=None, 
        names=columns
    )

    #file.write("DataFrame created\n")
    
    gen_test_df['txt_data'] = gen_test_df.user_json.apply(data_prep)
    gen_test_df.dropna(inplace = True)
  
    model_gender = pickle.load(open('/data/home/ruslan.tskhovrebadze/project01_model_logreg_gender.pickle', 'rb'))
    model_age = pickle.load(open('/data/home/ruslan.tskhovrebadze/project01_model_logreg_age.pickle', 'rb'))
    vectorizer = pickle.load(open('/data/home/ruslan.tskhovrebadze/project01_vectorizer.pickle', 'rb'))

    #file.write("Models imported\n")

    gen_test_vectorized = vectorizer.transform(gen_test_df['txt_data'].astype(str))
    
    #file.write("Data was vectorized\n")
    gen_pred_gender = model_gender.predict(gen_test_vectorized)
    #file.write("Gender was predicted\n")
    gen_pred_age = model_age.predict(gen_test_vectorized)
    #file.write("Age was predicted\n")

    gender_predict_proba = model_gender.predict_log_proba(gen_test_vectorized)
    age_predict_proba = model_age.predict_log_proba(gen_test_vectorized)
    
    gender_predict_proba_df = (pd.DataFrame(gender_predict_proba)).max(axis=1)
    age_predict_proba_df = (pd.DataFrame(age_predict_proba)).max(axis=1)
    
    res_df = pd.concat([gen_test_df, pd.DataFrame(gen_pred_gender, columns = {'pred_gender'}), 
                                      pd.DataFrame(gen_pred_age, columns = {'pred_age'})], axis = 1)

    res_df = pd.concat([res_df, gender_predict_proba_df, age_predict_proba_df], axis = 1) 
   
    
    #Подбор параметров отсечения записей по вероятности предсказания - чтобы с одной стороны подобрались предсказания с наибольшей вероятностью, 
    # с другой - тотчно набрать 50% пользователей
    gender_bottom= -0.45
    age_bottom = -1.0
        
    res_df['gender'] = res_df.apply(lambda row: row['pred_gender'] if (pd.to_numeric(row[0])> float(gender_bottom) and pd.to_numeric(row[1]) > float(age_bottom)) 
                                    else '-', axis=1)
    res_df['age'] = res_df.apply(lambda row: row['pred_age'] if (pd.to_numeric(row[0]) > float(gender_bottom) and pd.to_numeric(row[1]) > float(age_bottom)) 
                                    else '-', axis=1)   
    predicted_users = res_df[(res_df['gender'] != '-') & (res_df['age'] != '-')].count()/res_df.count() 

    while predicted_users['uid'] < 0.5:
        gender_bottom = gender_bottom - 0.001
        age_bottom = age_bottom - 0.003
        
        res_df.drop(columns = {'gender', 'age'}, inplace = True)
        
        res_df['gender'] = res_df.apply(lambda row: row['pred_gender'] if (row[0] > gender_bottom and row[1] > age_bottom) 
                                        else '-', axis=1)
        res_df['age'] = res_df.apply(lambda row: row['pred_age'] if (row[0] > gender_bottom and row[1] > age_bottom) 
                                     else '-', axis=1) 
        predicted_users = res_df[(res_df['gender'] != '-') & (res_df['age'] != '-')].count()/res_df.count()
        #file.write(str(predicted_users['uid']) + '\t' + str(gender_bottom) + '\t' + str(age_bottom) + '\n')

    #file.write("Treshold selection completed\n")     
 
    #file.write("Result dataframe formed\n")
    
    output = res_df[['uid', 'gender', 'age']]
    output.sort_values(by='uid',axis = 0, ascending = True, inplace = True)
    
    #file.write(output.to_json(orient='records'))
            
    sys.stdout.write(output.to_json(orient='records'))
    
    #file.write("Final JSON formed and transmitted\n")

except Exception as e:
    #file.write("Exception: {0} \n".format(str(e)))
    sys.stdout.write("Exception")