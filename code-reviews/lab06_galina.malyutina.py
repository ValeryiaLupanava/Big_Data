
# coding: utf-8

# In[1]:


import os
import sys
os.environ["PYSPARK_PYTHON"]='/opt/anaconda/envs/bd9/bin/python'
os.environ["SPARK_HOME"]='/usr/hdp/current/spark2-client'
os.environ["PYSPARK_SUBMIT_ARGS"]='--num-executors 3 pyspark-shell'

spark_home = os.environ.get('SPARK_HOME', None)

sys.path.insert(0, os.path.join(spark_home, 'python'))
sys.path.insert(0, os.path.join(spark_home, 'python/lib/py4j-0.10.7-src.zip'))


# In[2]:


from pyspark import SparkContext, SparkConf

conf = SparkConf()
conf.set("spark.app.name", "Lily Spark RDD lab06") 

sc = SparkContext(conf=conf)


# In[4]:


# читаем данные в RDD из файла
ml100 = sc.textFile("/labs/lab06data/ml-100k/u.data")
data = ml100.map(lambda x: tuple(x.split("\t"))).distinct().cache()


# In[5]:


# считаем hist_all
hist_all = data.map(lambda x: [x[2], 1])    .reduceByKey(lambda x, y: x + y)    .sortByKey()    .map(lambda x: x[1])    .cache()
hist_all.collect()


# In[6]:


# считаем hist_film
hist_film = data.filter(lambda x: x[1]=='328')    .map(lambda x: [x[2], 1])    .reduceByKey(lambda x, y: x + y)    .sortByKey()    .map(lambda x: x[1])    .cache()
hist_film.collect()


# In[7]:


# Готовим json
import json
final_dict = {'hist_all': hist_all.collect(), 'hist_film': hist_film.collect()}
json.dumps(final_dict)


# In[8]:


# Освобождаем воркеры
sc.stop()


# In[ ]:


# Лиля, привет. Код хорошо читаем. Мне, как  новичку, все понятно. Увидела, что  у себя забыла stop написать. 

