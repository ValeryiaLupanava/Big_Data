#Code Review
#Привет.
#1. Line 36-52 не совсем понятно, почему были эти колонки выбраны.
#2. Хотелось бы логики ограничения датасета в 100к строк из 300к. Сейчас пролучается, просто треть отбрасываем. 
#3. Хорошие комментарии и структура кода.
#Хорошего дня (:



#!/usr/bin/env python
# coding: utf-8

# In[1]:


# выбрал xgboost как наиболее эффективный по опыту
import pandas as pd
import xgboost as xgb


# In[2]:


train = pd.read_csv('lab04_train.csv')
train = train[train['TARGET'].notnull()] # убрал строки с нулевыми таргетами
test = pd.read_csv('lab04_test.csv')


# In[3]:


# ограничил строки в тренировочной выборке 100 000 т.к. комп пыхтел на 300 тыс.
X = train.iloc[:100000,2:116]
y = train.iloc[:100000,116]


# In[4]:


# по-хорошему, надо было эти колонки энкодить (см. запрос ниже), но он генерил десятки тысяч колонок
# к тому же, по опыту, энкодированные колонки мало влияют на эффективность, а ресурсов компа едят много
# поэтому решил их вырезать
col_to_encode = ['CLNT_TRUST_RELATION',
'APP_MARITAL_STATUS',
'APP_KIND_OF_PROP_HABITATION',
'CLNT_JOB_POSITION_TYPE',
'CLNT_JOB_POSITION',
'APP_EDUCATION',
'APP_TRAVEL_PASS',
'APP_POSITION_TYPE',
'APP_EMP_TYPE',
'APP_COMP_TYPE',
'APP_DRIVING_LICENSE',
'APP_CAR',
'PACK'               
]

# X = X.join(pd.get_dummies(X[col_to_encode]))
X = X.drop(col_to_encode, axis = 1)


# In[6]:


# не стал разбивать здесь на трейн тест сплит, т.к. в кросс валидации это будет сделано за меня
dtrain = xgb.DMatrix(X, label = y)


# In[7]:


# параметры (ключевые, которые больше всего влияют на эффективность - описаны в соотв строчках)
param = {
    "num_parallel_tree":1,
    "subsample":.9, # при бустинге каждого дерева мы берем не 100, а 90% строчек из датасета рандомно
    "colsample_bytree":.9,# при бустинге каждого дерева мы берем не 100, а 90% колонок из датасета рандомно
    "objective":"binary:logistic",
    "learning_rate":0.05, # шаг, по которому мы будем двигаться по функции снижения ошибки (большой - промажем, 
    # маленький - будем двигаться как черепаха и есть ресурсы компа)
    "eval_metric":"auc", 
    "max_depth":5, # глубина дерева
    "scale_pos_weight":len(y[y == 0]) / len(y[y == 1]),
    "min_child_weight":1,
    "seed":7
}


# In[8]:


#параметры кросс валидации
nfold = 5 # на сколько валидаций будем делить. В посл. лекции делили на 10, здесь - на 5
early_stopping_rounds = 5 # через сколько раундов остановим бустинг деревьев, если не увидим улучшения. 
stratified = True # распределим поровну нули и единицы между 5 нарезками 
n_estimators = 500 # сколько деревьев будем генерить


# In[9]:


# кросс-валидация
bst_cv = xgb.cv(
    param, 
    dtrain,  
    num_boost_round=n_estimators, 
    nfold = nfold,
    early_stopping_rounds=early_stopping_rounds,
    stratified = stratified
)


# In[10]:


# получаем отчет о рок-аук. Понимаем, что близко к тому, что в лабе
# берем для тренировки модели число раундов для бустинга (best_iteration) наиболее оптимальное с т.зр. кросс-валидации
# чтобы избежать переобучения и сэкономить ресурсы компа
# Еще std в выводе говорит, насколько велик разброс результатов каждой из 5 кросс-валидаций. 
# Если большой - модель нестабильна (переучена)
test_auc_mean = bst_cv["test-auc-mean"]
best_iteration = test_auc_mean[test_auc_mean == max(test_auc_mean)].index[0]

best_test_auc_mean = bst_cv["test-auc-mean"][best_iteration]
best_test_auc_mean_std = bst_cv["test-auc-std"][best_iteration]

print('''XGB CV model report
Best test-auc-mean {}% (std: {}%)'''.format(round(best_test_auc_mean * 100, 2), 
                                          round(best_test_auc_mean_std * 100, 2)))


# In[11]:


# тренируем модель
bst = xgb.train(param, 
                    dtrain, 
                    num_boost_round = best_iteration)


# In[12]:


ids = test.ID
# предсказываем на тестовой выборке
pred_test = test.iloc[:,2:116]
pred_test = pred_test.drop(col_to_encode, axis = 1)
pred_test = xgb.DMatrix(pred_test)
pred = pd.Series(bst.predict(pred_test))


# In[20]:


# объединяем id и предсказания
res = pd.concat([ids, pred], axis=1)
# переименовываем колонки
res.rename(columns={'ID': "id", 0: "target"}, inplace=True)


# In[25]:


# сохраняем.
res.to_csv("lab04.csv", sep='\t', index=False)

# roc auc 0.83
