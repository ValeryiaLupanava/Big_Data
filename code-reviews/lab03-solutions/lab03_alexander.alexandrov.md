### Запуск
```
$ beeline -u jdbc:hive2://bd-node1.newprolab.com:10000 \
$  -n alexander.alexandrov \
$  --outputformat=tsv2 \
$  --showHeader=false \
$  -f job.hql > ~/lab03_users.txt
```

### Создание таблицы
Предварительно скопировал данные себе во временную папку. Прав на создание external table в location '/labs/lab03data' не было. В идеальном случае надо делать external table сразу на локацию '/labs/lab03data', чтобы не дублировать данные.

```
hdfs dfs -cp /labs/lab03data /tmp/alexander.alexandrov/lab03/lab03data
```

Создание таблицы для запросов
```
create external table lab03data(
  `UID` bigint,
  `timestamp` double,
  `URL` string
)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY '\t'
stored as textfile
location '/tmp/alexander.alexandrov/lab03/lab03data'
```


### Скрипт формирования job.sql

Делал в один запрос. Возможно, выглядит громоздко, но, как мне кажется, одно из самых быстрых по производительности решений.
```
with data as (
  select
    d.uid, 
    regexp_replace(parse_url(regexp_replace(regexp_replace(d.url, '%3A', ':'), '%2F', '/'), 'HOST'), '^www.', '') host, 
    count(1)
   from alexander_alexandrov.lab03data d
  where d.uid is not null
    and d.url rlike '(^http|^https){1}(%3A|:){1}(%2F|/){2}'
    and regexp_replace(parse_url(regexp_replace(regexp_replace(d.url, '%3A', ':'), '%2F', '/'), 'HOST'), '^www.', '') in ('cars.ru', 'avto-russia.ru', 'bmwclub.ru', 'samara-papa.ru', 'vodvore.net', 'mama51.ru', 'sp.krasmama.ru', 'forum.krasmama.ru', 'forum.omskmama.ru', 'novayagazeta.ru', 'echo.msk.ru', 'inosmi.ru')
  group by d.uid, regexp_replace(parse_url(regexp_replace(regexp_replace(d.url, '%3A', ':'), '%2F', '/'), 'HOST'), '^www.', '')
  having count(1) >= 10
)
select
  d.uid,
  max(case when d.host in ('cars.ru', 'avto-russia.ru', 'bmwclub.ru') then 1 else 0 end) user_cat1_flag,
  max(case when d.host in ('samara-papa.ru', 'vodvore.net', 'mama51.ru') then 1 else 0 end) user_cat2_flag,
  max(case when d.host in ('sp.krasmama.ru', 'forum.krasmama.ru', 'forum.omskmama.ru') then 1 else 0 end) user_cat3_flag,
  max(case when d.host in ('novayagazeta.ru', 'echo.msk.ru', 'inosmi.ru') then 1 else 0 end) user_cat4_flag
from data d
group by d.uid
order by d.uid;
```
