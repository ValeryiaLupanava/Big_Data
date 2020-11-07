# Лабараторная №04

Подключаю библиотеки
```python
import pandas as pd
import numpy as np
```

Функция для преобразования выборки. Не очень оптимально, но тогда мой пандас был совсем плохой.
```python
def one_hot(data):
    del data['APP_COMP_TYPE']
    del data['APP_DRIVING_LICENSE']
    del data['APP_EDUCATION']
    del data['APP_EMP_TYPE']
    del data['APP_KIND_OF_PROP_HABITATION']
    del data['APP_MARITAL_STATUS']
    del data['CLNT_TRUST_RELATION']
    del data['APP_POSITION_TYPE']
    del data['APP_CAR']
    del data['APP_TRAVEL_PASS']
    del data['CLNT_JOB_POSITION']
    del data['CLNT_JOB_POSITION_TYPE']
    data = pd.get_dummies(data, columns=['PACK'])
    data = data.drop(['PACK_108'], axis=1, errors='ignore')
    data = data.fillna(0)
    return data
 ```   

Открою файл с исходными данными и подготовлю их для обучения
```python
data = pd.read_csv('lab04_train.csv')

data = one_hot(data)
df = data[:-1] # откусим заголовок
target = df['TARGET']
del df['TARGET']

test = pd.read_csv('lab04_test.csv')
test = one_hot(test)
```

Делим на выборки и начем обучение
```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df, target, test_size=0.2)
print(len(X_train), len(X_test), len(y_train), len(y_test))

from sklearn.ensemble import RandomForestClassifier
lr = RandomForestClassifier(n_estimators=1000, n_jobs=4, verbose=True, )
lr.fit(X_train, y_train)
```

Проверим, что все хорошо на исходной выборке и оценим качество обучение на тестовой выборке

```python
pred_train = lr.predict_proba(X_train)
pred_test = lr.predict_proba(X_test)
roc_auc_score( y_train, pred_train[:,1]), roc_auc_score( y_test, pred_test[:,1])
```

Ещё раз обучим рандомфорест уже на всех данных, и создадим файл с финальными данными для сдачи лабораторной работы
```python
lr = RandomForestClassifier(n_estimators= 10000, n_jobs=8, verbose=True, )
lr.fit(df, target)

result = lr.predict_proba(test)[:,1]

test2 = test.copy()
test2['TARGET'] = result
test2=test2.rename(columns={'ID': 'id', 'TARGET': 'target'})
test2[['id', 'target']].to_csv("lab04s.csv", sep="\t", index=False) 
```

ROC-AUC 0.839186286861