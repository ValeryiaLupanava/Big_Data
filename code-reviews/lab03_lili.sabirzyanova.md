## Решение лабы 3
**Первый этап очистки данных я сделал с помощью hadoop map reduce. Не стал приводить код, т.к. лаба по hive**  
`hadoop jar ./hadoop-streaming.jar -D mapred.reduce.tasks=0 -files=app -input /labs/lab03data/* -output /user/alexander.prutko/lab03/data -mapper "app/mapper.py"`

**Задание я выполнял следующим образом: сначала запускал hql, который записывал результат в файл, потом на основе получившегося файла создавал таблицу в hive, с которой уже в дальнейшем работал. Разбил выполнение задачи на последовательные шаги**

#### Создание таблицы "visits" на основе выхода map reduce задачи - очищенные посещения сайтов пользователями
* uid - уникальный идентификатор пользователя
* url - домен посещенного сайта  
```create external table visits
(
uid bigint,
url string
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'
LOCATION '/user/alexander.prutko/lab03/data';
```

#### Нахождение всех пользователей, посетивших один из 12 доменов хотя бы 10 раз. Записывается кто посетил какой сайт и сколько раз (если >=10)
```insert overwrite directory 'hdfs://bd-master.newprolab.com:8020/user/alexander.prutko/lab03/counts'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
select cast(uid as bigint), url, count(*) as cnt from visits where
url='cars.ru' or
url='avto-russia.ru' or
url='bmwclub.ru' or
url='postnauka.ru' or 
url='plantarium.ru' or
url='lensart.ru' or
url='pass.rzd.ru' or
url='rzd.ru' or
url='vokrug.tv' or
url='apteka.ru' or
url='doctor.ufacity.info' or
url='womanhit.ru'
group by uid, url
having cnt>=10
order by uid;
```
@@ Рекомендую в будущем использовать конструкцию `url` in (domain1, domain2, ... )@@


#### Создание таблицы "counts" на основе предыдущего шага
* uid - уникальный идентификатор пользователя
* url - домен посещенного сайта
* cnt - сколько раз пользователь посетил сайт  
```create external table counts
(
uid bigint,
url string,
count int
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'
LOCATION '/user/alexander.prutko/lab03/counts';
```

#### Нахождение всех пользователей, относящихся к категории "автомобилисты"
```insert overwrite directory 'hdfs://bd-master.newprolab.com:8020/user/alexander.prutko/lab03/auto'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
select distinct cast(uid as bigint), 1 as id1 from counts where
url='cars.ru' or
url='avto-russia.ru' or
url='bmwclub.ru';
```

#### Создание таблицы "auto" на основе предыдущего шага
* uid - уникальный идентификатор пользователя
* auto - признак автомобилиста = 1  
```create external table auto
(
uid bigint,
auto int
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'
LOCATION '/user/alexander.prutko/lab03/auto';
```

#### Нахождение всех пользователей, относящихся к категории "культурные люди"
```insert overwrite directory 'hdfs://bd-master.newprolab.com:8020/user/alexander.prutko/lab03/culture'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
select distinct cast(uid as bigint), 1 as id2 from counts where
url='postnauka.ru' or
url='plantarium.ru' or
url='lensart.ru';
```

#### Создание таблицы "culture" на основе предыдущего шага
* uid - уникальный идентификатор пользователя
* culture - признак культурного человека = 1  
```create external table culture
(
uid bigint,
culture int
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'
LOCATION '/user/alexander.prutko/lab03/culture'; 
```

#### Нахождение всех пользователей, относящихся к категории "путешественники"
```insert overwrite directory 'hdfs://bd-master.newprolab.com:8020/user/alexander.prutko/lab03/travel'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
select distinct cast(uid as bigint), 1 as id3 from counts where
url='pass.rzd.ru' or
url='rzd.ru' or
url='vokrug.tv';
```

#### Создание таблицы "travel" на основе предыдущего шага
* uid - уникальный идентификатор пользователя
* travel - признак путешественника = 1  
```create external table travel
(
uid bigint,
travel int
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'
LOCATION '/user/alexander.prutko/lab03/travel';  
```

#### Нахождение всех пользователей, относящихся к категории "больные люди"
```insert overwrite directory 'hdfs://bd-master.newprolab.com:8020/user/alexander.prutko/lab03/sick'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
select distinct cast(uid as bigint), 1 as id4 from counts where
url='apteka.ru' or
url='doctor.ufacity.info' or
url='womanhit.ru';
```

#### Создание таблицы "sick" на основе предыдущего шага
* uid - уникальный идентификатор пользователя
* sick - признак больного человека = 1  
```create external table sick
(
uid bigint,
sick int
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'
LOCATION '/user/alexander.prutko/lab03/sick';
```
@@ Тут напрашивается либо view с параметрами, либо один большй запрос, который посчитает сразу все 4 группы.@@


#### Составление сводной таблицы со всеми пользователями со столбцами **auto**, **culture**, **travel** и **sick**. 1 - пользователь относится к категории, 0 - не относится
```insert overwrite directory 'hdfs://bd-master.newprolab.com:8020/user/alexander.prutko/lab03/result'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
select cast(v.uid as bigint) as uid, coalesce(a.auto, 0) as auto,
                                   coalesce(c.culture, 0) as culture,
                                   coalesce(t.travel, 0) as travel,
                                   coalesce(s.sick, 0) as sick
from
(
(select distinct uid from visits) v
left join
auto a
on v.uid=a.uid
left join
culture c
on v.uid=c.uid
left join
travel t
on v.uid=t.uid
left join
sick s
on v.uid=s.uid
) order by uid;
```
@@ Вложенный запрос совершенно лишний, можно было написать SELECT ... FROM `visits` v LEFT JOIN ... @@


#### Создание таблицы "cats" на основе предыдущего шага
* uid - уникальный идентификатор пользователя
* auto - признак автомобилиста = 1
* culture - признак культурного человека = 1
* travel - признак путешественника = 1
* sick - признак больного человека = 1  
```create external table cats
(
uid bigint,
auto int,
culture int,
travel int,
sick int
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'
LOCATION '/user/alexander.prutko/lab03/result';
```

@@ Промежуточные таблички можно было бы хранить во внутренних директориях хайва, что бы не заморачиваться с их созданием, но тут уже кому как удобнее.@@