
# coding: utf-8

# In[5]:


import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split
from sklearn.metrics import roc_auc_score
import xgboost


# In[6]:


# работа с train

train = pd.read_csv(r'/data/share/lab04data/lab04_train.csv')  
train = train[train['TARGET'].notnull()]
X = train
col_for_del = ['APP_CAR','APP_COMP_TYPE','APP_DRIVING_LICENSE','APP_EDUCATION','APP_EMP_TYPE','APP_KIND_OF_PROP_HABITATION',
'APP_MARITAL_STATUS','APP_POSITION_TYPE','APP_TRAVEL_PASS','CLNT_JOB_POSITION','CLNT_JOB_POSITION_TYPE','CLNT_TRUST_RELATION',
'PACK']

X=X.drop(col_for_del,axis=1)
X[np.isnan(X)] = 0
X = X.drop('TARGET', axis=1)
y = train['TARGET']


# In[7]:


# работа с test
test = pd.read_csv(r'/data/share/lab04data/lab04_test.csv')  

col_for_del = ['APP_CAR','APP_COMP_TYPE','APP_DRIVING_LICENSE','APP_EDUCATION','APP_EMP_TYPE','APP_KIND_OF_PROP_HABITATION',
'APP_MARITAL_STATUS','APP_POSITION_TYPE','APP_TRAVEL_PASS','CLNT_JOB_POSITION','CLNT_JOB_POSITION_TYPE','CLNT_TRUST_RELATION',
'PACK']

test=test.drop(col_for_del,axis=1)
test[np.isnan(test)] = 0


# In[ ]:


# сразу обучение
model = xgboost.XGBClassifier(max_depth=10)
model.fit(X, y)
pred_test = model.predict_proba(test)[:,1]
# копирование в файл
output=pd.DataFrame(data = {'id':test['ID'],'target':pred_test}) 
output.to_csv(path_or_buf = "lab04.csv",index=False,sep='\t')


# In[4]:


# для проверки обучения
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=30)

model = xgboost.XGBClassifier(max_depth=10)
model.fit(X_train, y_train)
pred = model.predict_proba(X_test)[:,1]
roc_auc_score(y_test, pred)


# In[5]:


model = xgboost.XGBClassifier(max_depth=10)
model.fit(X_train, y_train)


# In[6]:


pred = model.predict_proba(X_test)[:,1]


# In[7]:


roc_auc_score(y_test, pred)

