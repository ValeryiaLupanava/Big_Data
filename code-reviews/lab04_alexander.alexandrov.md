
# Лаба 4. Спрогнозировать отток клиентов банка по историческим данным


```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
```

## Шаг 1. Чтение данных train


```python
%%time
train_data = pd.read_csv('/data/share/lab04data/lab04_train.csv', sep=',')
test_data = pd.read_csv('/data/share/lab04data/lab04_test.csv', sep=',')
```

    CPU times: user 20.2 s, sys: 8.28 s, total: 28.4 s
    Wall time: 7.9 s



```python
train_data.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Unnamed: 0</th>
      <th>ID</th>
      <th>CR_PROD_CNT_IL</th>
      <th>AMOUNT_RUB_CLO_PRC</th>
      <th>PRC_ACCEPTS_A_EMAIL_LINK</th>
      <th>APP_REGISTR_RGN_CODE</th>
      <th>PRC_ACCEPTS_A_POS</th>
      <th>PRC_ACCEPTS_A_TK</th>
      <th>TURNOVER_DYNAMIC_IL_1M</th>
      <th>CNT_TRAN_AUT_TENDENCY1M</th>
      <th>...</th>
      <th>REST_DYNAMIC_CC_3M</th>
      <th>MED_DEBT_PRC_YWZ</th>
      <th>LDEAL_ACT_DAYS_PCT_TR3</th>
      <th>LDEAL_ACT_DAYS_PCT_AAVG</th>
      <th>LDEAL_DELINQ_PER_MAXYWZ</th>
      <th>TURNOVER_DYNAMIC_CC_3M</th>
      <th>LDEAL_ACT_DAYS_PCT_TR</th>
      <th>LDEAL_ACT_DAYS_PCT_TR4</th>
      <th>LDEAL_ACT_DAYS_PCT_CURR</th>
      <th>TARGET</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>333149</td>
      <td>479990</td>
      <td>0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>303639</td>
      <td>450480</td>
      <td>0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>327113</td>
      <td>473954</td>
      <td>0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>384197</td>
      <td>531038</td>
      <td>0</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>...</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>202462</td>
      <td>349303</td>
      <td>0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>...</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 117 columns</p>
</div>




```python
test_data.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Unnamed: 0</th>
      <th>ID</th>
      <th>CR_PROD_CNT_IL</th>
      <th>AMOUNT_RUB_CLO_PRC</th>
      <th>PRC_ACCEPTS_A_EMAIL_LINK</th>
      <th>APP_REGISTR_RGN_CODE</th>
      <th>PRC_ACCEPTS_A_POS</th>
      <th>PRC_ACCEPTS_A_TK</th>
      <th>TURNOVER_DYNAMIC_IL_1M</th>
      <th>CNT_TRAN_AUT_TENDENCY1M</th>
      <th>...</th>
      <th>LDEAL_ACT_DAYS_ACC_PCT_AVG</th>
      <th>REST_DYNAMIC_CC_3M</th>
      <th>MED_DEBT_PRC_YWZ</th>
      <th>LDEAL_ACT_DAYS_PCT_TR3</th>
      <th>LDEAL_ACT_DAYS_PCT_AAVG</th>
      <th>LDEAL_DELINQ_PER_MAXYWZ</th>
      <th>TURNOVER_DYNAMIC_CC_3M</th>
      <th>LDEAL_ACT_DAYS_PCT_TR</th>
      <th>LDEAL_ACT_DAYS_PCT_TR4</th>
      <th>LDEAL_ACT_DAYS_PCT_CURR</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>372289</td>
      <td>519130</td>
      <td>0</td>
      <td>0.000000</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>87204</td>
      <td>234045</td>
      <td>0</td>
      <td>0.013322</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>254415</td>
      <td>401256</td>
      <td>0</td>
      <td>0.011870</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.666667</td>
      <td>...</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>404229</td>
      <td>551070</td>
      <td>0</td>
      <td>0.000000</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>220444</td>
      <td>367285</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 116 columns</p>
</div>



## Шаг 2. Очистка данных и подготовка к обучению


```python
#копируем целевую переменную и объединяем train и test данные для совместной обработки
y_train = train_data['TARGET'].fillna(0) # в данных есть немного мусора - целевая переменная NAN - заполним нулем
train_data.drop(['TARGET'], axis=1, inplace=True)
```


```python
train_data.shape, test_data.shape
```




    ((320764, 116), (44399, 116))




```python
# Объединяем данные для удобства
joined_data = pd.concat([train_data, test_data])
```


```python
joined_data.shape
```




    (365163, 116)




```python
%%time
#заполняем пропуски нулями для колонок INT и FLOAT и NA для строковых колонок
clean_joined_data = pd.concat([
    joined_data.loc[:, joined_data.dtypes==np.object].fillna('NA'),
    joined_data.loc[:, joined_data.dtypes==np.float64].fillna(0),
    joined_data.loc[:, joined_data.dtypes==np.int64].fillna(0),
    ], axis=1)
```

    CPU times: user 26 s, sys: 7.02 s, total: 33 s
    Wall time: 2.24 s



```python
# удаляем ненужные \ неинформативные колонки
clean_data = clean_joined_data.drop(['ID','Unnamed: 0','CLNT_JOB_POSITION'], axis=1)
# Фича 'CLNT_JOB_POSITION' потенциально полезная, до конца не хотел удалять, но в конце концов несет больше шума, чем пользы. 
# Если подумать как преобразовать эти данные и удалить шум, то можно будет вернуть (возможно, нужна иерархия, как в событиях IVR)
```


```python
clean_data.shape
```




    (365163, 113)




```python
%%time
# масштабирование
clean_data_dum = StandardScaler().fit_transform(clean_data_dum)
```

    CPU times: user 1min 4s, sys: 28.8 s, total: 1min 33s
    Wall time: 4.21 s



```python
# теперь разбиваем очищенные данные обратно на train и test. 
## Поскольку мы строки не сортировали, то у нас сначала идут строки от train, а потом от test
assert train_data.shape[0] + test_data.shape[0] == clean_data_dum.shape[0]

x_train, x_test = clean_data_dum[:train_data.shape[0]], \
                  clean_data_dum[train_data.shape[0]:]
```


```python
# проверка, что все корректно разбилось
train_data.shape[0], test_data.shape[0], x_train.shape, x_test.shape, y_train.shape
```




    (320764, 44399, (320764, 204), (44399, 204), (320764,))



## Шаг 3. Строим модель XGBOOST
(на чисто академических задачах (Kaggle,...) всегда меня спасала)


```python
import xgboost as xgb
```


```python
y_train.unique()
```




    array([0., 1.])




```python
%%time
from sklearn.model_selection import GridSearchCV
xgb_model = xgb.XGBClassifier()
parameters = {
    'nthread'            : [4],
    'objective'          : ['binary:logistic'],
    'learning_rate'      : [0.05, 0.1, 0.2, 0.3, 0.5], # иногда в пакетах называется 'eta'
    'max_depth'          : [5,7],
    'min_child_weight'   : [ 1, 3, 5, 7, 11],
    #'gamma'              : [ 0.0, 0.1, 0.2, 0.3, 0.4],
    #'colsample_bytree'   : [ 0.3, 0.4, 0.5, 0.7],
    'n_estimators'       : [100] # тестируем при 100, в прод сделаем этот параметр равным 1000 для большей точности
     }
clf = GridSearchCV(xgb_model, parameters, n_jobs=5,
                   scoring="roc_auc",
                   cv=3,
                   verbose=2)
clf.fit(x_train, y_train)

#вытаскиваем результаты тюнинга моделей
best_parameters, score, _ = max(clf.grid_scores_, key=lambda x: x[1])
print('ROC AUC score:', score)
for param_name in sorted(best_parameters.keys()):
    print("%s: %r" % (param_name, best_parameters[param_name]))
```

    Fitting 3 folds for each of 50 candidates, totalling 150 fits
    [CV] learning_rate=0.05, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV] learning_rate=0.05, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV] learning_rate=0.05, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV] learning_rate=0.05, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV] learning_rate=0.05, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total=  54.7s
    [CV] learning_rate=0.05, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.0min
    [CV] learning_rate=0.05, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.0min
    [CV] learning_rate=0.05, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.0min
    [CV] learning_rate=0.05, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.0min
    [CV] learning_rate=0.05, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total=  53.0s
    [CV] learning_rate=0.05, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total=  54.7s
    [CV] learning_rate=0.05, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total=  55.9s
    [CV] learning_rate=0.05, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total=  53.5s
    [CV] learning_rate=0.05, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total=  54.3s
    [CV] learning_rate=0.05, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total=  54.2s
    [CV] learning_rate=0.05, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total=  58.1s
    [CV] learning_rate=0.05, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.0min
    [CV] learning_rate=0.05, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.2min
    [CV] learning_rate=0.05, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.1min
    [CV] learning_rate=0.05, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.05, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.4min
    [CV] learning_rate=0.05, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.4min
    [CV] learning_rate=0.05, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.4min
    [CV] learning_rate=0.05, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.4min
    [CV] learning_rate=0.05, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.4min
    [CV] learning_rate=0.05, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.05, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.05, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.7min
    [CV]  learning_rate=0.05, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.6min
    [CV] learning_rate=0.05, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV] learning_rate=0.05, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.6min
    [CV] learning_rate=0.1, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.6min
    [CV] learning_rate=0.1, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total= 2.0min
    [CV] learning_rate=0.1, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.4min
    [CV] learning_rate=0.1, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.05, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.4min
    [CV] learning_rate=0.1, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.0min
    [CV] learning_rate=0.1, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 


    [Parallel(n_jobs=5)]: Done  31 tasks      | elapsed:  8.4min


    [CV]  learning_rate=0.1, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.1min
    [CV] learning_rate=0.1, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total=  54.7s
    [CV] learning_rate=0.1, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total=  53.8s
    [CV] learning_rate=0.1, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total=  54.7s
    [CV] learning_rate=0.1, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.1min
    [CV] learning_rate=0.1, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.0min
    [CV] learning_rate=0.1, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.2min
    [CV] learning_rate=0.1, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.2min
    [CV] learning_rate=0.1, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.1, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.1min
    [CV] learning_rate=0.1, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.2min
    [CV] learning_rate=0.1, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total=  55.3s
    [CV] learning_rate=0.1, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total=  55.8s
    [CV] learning_rate=0.1, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total=  55.6s
    [CV] learning_rate=0.1, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.1, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.1, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.2min
    [CV] learning_rate=0.1, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.1, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.1, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.8min
    [CV] learning_rate=0.1, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total= 2.0min
    [CV] learning_rate=0.1, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.9min
    [CV] learning_rate=0.1, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total= 2.2min
    [CV] learning_rate=0.1, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total= 2.3min
    [CV] learning_rate=0.1, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.6min
    [CV] learning_rate=0.2, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.5min
    [CV] learning_rate=0.2, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.2, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.2, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.1, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.2, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total=  55.2s
    [CV] learning_rate=0.2, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total=  55.8s
    [CV] learning_rate=0.2, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total=  53.9s
    [CV] learning_rate=0.2, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total=  54.6s
    [CV] learning_rate=0.2, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total=  52.8s
    [CV] learning_rate=0.2, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total=  51.3s
    [CV] learning_rate=0.2, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total=  52.6s
    [CV] learning_rate=0.2, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total=  53.1s
    [CV] learning_rate=0.2, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total=  53.0s
    [CV] learning_rate=0.2, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total=  52.6s
    [CV] learning_rate=0.2, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total=  52.7s
    [CV] learning_rate=0.2, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total=  54.0s
    [CV] learning_rate=0.2, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total=  53.7s
    [CV] learning_rate=0.2, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total=  54.4s
    [CV] learning_rate=0.2, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total=  53.7s
    [CV] learning_rate=0.2, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.2min
    [CV] learning_rate=0.2, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.2min
    [CV] learning_rate=0.2, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.2, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.2, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.2, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.2min
    [CV] learning_rate=0.2, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV]  learning_rate=0.2, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.4min
    [CV] learning_rate=0.2, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV] learning_rate=0.2, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.2, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.2min
    [CV] learning_rate=0.2, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.3, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.3, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.3, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.3, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.2, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.3, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total=  58.5s
    [CV] learning_rate=0.3, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.7min
    [CV] learning_rate=0.3, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.7min
    [CV] learning_rate=0.3, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.7min
    [CV] learning_rate=0.3, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.7min
    [CV] learning_rate=0.3, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total= 2.0min
    [CV] learning_rate=0.3, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.1min
    [CV] learning_rate=0.3, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.0min
    [CV] learning_rate=0.3, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.0min
    [CV] learning_rate=0.3, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.0min
    [CV] learning_rate=0.3, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total=  55.1s
    [CV] learning_rate=0.3, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total=  55.1s
    [CV] learning_rate=0.3, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total=  55.4s
    [CV] learning_rate=0.3, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total=  56.0s
    [CV] learning_rate=0.3, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total=  54.9s
    [CV] learning_rate=0.3, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.3, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.6min
    [CV] learning_rate=0.3, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.6min
    [CV] learning_rate=0.3, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.7min
    [CV] learning_rate=0.3, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.7min
    [CV] learning_rate=0.3, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.8min
    [CV] learning_rate=0.3, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.5min
    [CV] learning_rate=0.3, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.4min
    [CV] learning_rate=0.3, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.4min
    [CV] learning_rate=0.3, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.3, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.2min
    [CV] learning_rate=0.5, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.2min
    [CV] learning_rate=0.5, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.5, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.2min
    [CV] learning_rate=0.5, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.3, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.5, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total=  53.4s
    [CV] learning_rate=0.5, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total=  53.8s
    [CV] learning_rate=0.5, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=5, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total=  53.1s
    [CV] learning_rate=0.5, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total=  53.8s
    [CV] learning_rate=0.5, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total=  53.8s
    [CV] learning_rate=0.5, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=5, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total=  52.4s
    [CV] learning_rate=0.5, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total=  53.0s
    [CV] learning_rate=0.5, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total=  53.3s
    [CV] learning_rate=0.5, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=5, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total=  53.0s
    [CV] learning_rate=0.5, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total=  53.3s
    [CV] learning_rate=0.5, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total=  52.7s
    [CV] learning_rate=0.5, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=5, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total=  53.9s
    [CV] learning_rate=0.5, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total=  55.8s
    [CV] learning_rate=0.5, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total=  54.5s
    [CV] learning_rate=0.5, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=5, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total=  55.3s
    [CV] learning_rate=0.5, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.2min
    [CV] learning_rate=0.5, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.2min
    [CV] learning_rate=0.5, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=7, min_child_weight=1, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.2min
    [CV] learning_rate=0.5, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.2min
    [CV] learning_rate=0.5, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.2min
    [CV] learning_rate=0.5, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=7, min_child_weight=3, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.2min
    [CV] learning_rate=0.5, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.5, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.5, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=7, min_child_weight=5, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.3min
    [CV] learning_rate=0.5, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total= 1.5min
    [CV] learning_rate=0.5, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic 
    [CV]  learning_rate=0.5, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total= 2.1min
    [CV]  learning_rate=0.5, max_depth=7, min_child_weight=7, n_estimators=100, nthread=4, objective=binary:logistic, total= 2.5min
    [CV]  learning_rate=0.5, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total= 2.5min
    [CV]  learning_rate=0.5, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total= 2.6min
    [CV]  learning_rate=0.5, max_depth=7, min_child_weight=11, n_estimators=100, nthread=4, objective=binary:logistic, total= 2.3min


    [Parallel(n_jobs=5)]: Done 150 out of 150 | elapsed: 39.2min finished


    ROC AUC score: 0.8520747333023739
    learning_rate: 0.2
    max_depth: 7
    min_child_weight: 11
    n_estimators: 100
    nthread: 4
    objective: 'binary:logistic'
    CPU times: user 13min 31s, sys: 1min 48s, total: 15min 19s
    Wall time: 41min 31s


    /opt/anaconda/envs/bd9/lib/python3.6/site-packages/sklearn/model_selection/_search.py:762: DeprecationWarning: The grid_scores_ attribute was deprecated in version 0.18 in favor of the more elaborate cv_results_ attribute. The grid_scores_ attribute will not be available from 0.20
      DeprecationWarning)


### Есть контакт!!!! Требования лаб 04 и 04s выполнены


```python
cv_data = xgb.DMatrix(x_train, label = y_train)
```


```python
%%time
##кросс-валидация, еще раз проверим
best_parameters = {
    'nthread'            : 4,
    'objective'          : 'binary:logistic',
    'learning_rate'      : 0.2,
    'max_depth'          : 7,
    'min_child_weight'   : 11,
    'n_estimators'       : 1000
}
xgb_cv = xgb.cv(best_parameters, cv_data, nfold = 5, metrics = {'auc'}, seed = 7)
```

    [21:28:52] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 240 extra nodes, 0 pruned nodes, max_depth=7
    [21:28:55] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 236 extra nodes, 0 pruned nodes, max_depth=7
    [21:28:57] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 238 extra nodes, 0 pruned nodes, max_depth=7
    [21:28:59] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 236 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:02] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 236 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:03] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 238 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:03] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 238 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:04] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 240 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:05] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 222 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:06] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 228 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:07] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 232 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:07] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 232 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:08] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 232 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:09] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 240 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:10] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 232 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:11] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 226 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:11] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 228 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:12] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 230 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:13] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 226 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:14] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 240 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:15] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 236 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:15] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 222 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:16] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 236 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:17] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 230 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:18] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 232 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:19] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 230 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:19] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 224 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:20] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 224 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:21] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 240 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:22] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 222 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:23] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 214 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:23] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 232 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:24] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 216 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:25] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 224 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:26] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 218 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:27] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 230 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:28] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 224 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:29] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 228 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:30] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 218 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:31] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 226 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:32] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 232 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:32] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 224 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:33] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 238 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:34] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 214 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:35] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 222 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:36] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 228 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:37] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 208 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:37] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 222 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:38] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 210 extra nodes, 0 pruned nodes, max_depth=7
    [21:29:39] src/tree/updater_prune.cc:74: tree pruning end, 1 roots, 220 extra nodes, 0 pruned nodes, max_depth=7
    CPU times: user 3min 7s, sys: 12.2 s, total: 3min 19s
    Wall time: 1min 3s



```python
xgb_cv
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>train-auc-mean</th>
      <th>train-auc-std</th>
      <th>test-auc-mean</th>
      <th>test-auc-std</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.814380</td>
      <td>0.000396</td>
      <td>0.803633</td>
      <td>0.002108</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.825051</td>
      <td>0.001453</td>
      <td>0.814366</td>
      <td>0.002172</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.830512</td>
      <td>0.001267</td>
      <td>0.818507</td>
      <td>0.001755</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.834298</td>
      <td>0.000878</td>
      <td>0.821795</td>
      <td>0.002184</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.836998</td>
      <td>0.000812</td>
      <td>0.823831</td>
      <td>0.001914</td>
    </tr>
    <tr>
      <th>5</th>
      <td>0.839205</td>
      <td>0.000550</td>
      <td>0.825398</td>
      <td>0.002136</td>
    </tr>
    <tr>
      <th>6</th>
      <td>0.841443</td>
      <td>0.000827</td>
      <td>0.827110</td>
      <td>0.001879</td>
    </tr>
    <tr>
      <th>7</th>
      <td>0.843284</td>
      <td>0.000857</td>
      <td>0.828424</td>
      <td>0.001980</td>
    </tr>
    <tr>
      <th>8</th>
      <td>0.845404</td>
      <td>0.000782</td>
      <td>0.830173</td>
      <td>0.001887</td>
    </tr>
    <tr>
      <th>9</th>
      <td>0.847125</td>
      <td>0.000904</td>
      <td>0.831360</td>
      <td>0.001859</td>
    </tr>
  </tbody>
</table>
</div>



#### Oбучение


```python
Final_clf = xgb.XGBClassifier(max_depth = 7,
                              learning_rate = 0.2,
                              n_estimators = 1000,
                              objective='binary:logistic',
                              nthread = 4,
                              min_child_weight = 11)
```


```python
%%time
# обучаем
Final_clf.fit(x_train, y_train)
```

    CPU times: user 1h 3min 46s, sys: 4.45 s, total: 1h 3min 51s
    Wall time: 16min 11s





    XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
           colsample_bytree=1, gamma=0, learning_rate=0.2, max_delta_step=0,
           max_depth=7, min_child_weight=11, missing=None, n_estimators=1000,
           n_jobs=1, nthread=4, objective='binary:logistic', random_state=0,
           reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None,
           silent=True, subsample=1)



### Шаг 4. Классификация по тестовой выборке и сохранение результатов в файл


```python
x_test.shape, x_train.shape
```




    ((44399, 204), (320764, 204))




```python
predict = Final_clf.predict_proba(x_test)
```


```python
pd.DataFrame(predict).head()
pd.DataFrame(predict).shape
```




    (44399, 2)




```python
pd.DataFrame(
    {'id':test_data['ID'].values, 
     'target':predict[:,1]}
).to_csv('/data/home/alexander.dorofeyev/lab04.csv', 
         index=False, 
         sep='\t')
```


```python
pd.DataFrame(
    {'id':test_data['ID'].values, 
     'target':predict[:,1]}
).to_csv('/data/home/alexander.dorofeyev/lab04s.csv', 
         index=False, 
         sep='\t')
```

# THE END!!!

# Code review

На самом деле даже не знаю, что добавить по алгоритму. Если по самому коду, то, возможно, конструкции вида 
```python
pd.DataFrame(predict).head()
pd.DataFrame(predict).shape
```

Лучше заменить через переменную на
```python
predic_df = pd.DataFrame(predict)
predic_df.head()
predic_df.shape
```
Но это просто для повышения читабельности, на функционал никак не влияет :)