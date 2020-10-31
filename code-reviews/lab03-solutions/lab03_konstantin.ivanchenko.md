# Подключение к Hive:
beeline jdbc:hive2://bd-node1.newprolab.com:10000 -n hive

# Переключение на свою базу:
use konstantin_ivanchenko;

# Создание таблицы:
CREATE EXTERNAL TABLE source_data
(
 uid bigint,
 tstamp string,
 url string
)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE;

# Заливка в таблицу данных из файла
LOAD DATA INPATH '/tmp/konstantin.ivanchenko/hive/lab03data/' INTO TABLE source_data;

# Формирование результирующей таблицы:
create external table lab03_users
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
as
with t as (
select 
  uid,
  case 
    when substr(parse_url(replace(replace(url,'%3A',':'),'%2F','/'),'HOST'),1,4) = 'www.'
      then substr(parse_url(replace(replace(url,'%3A',':'),'%2F','/'),'HOST'),5)
      else parse_url(replace(replace(url,'%3A',':'),'%2F','/'),'HOST')
  end as url,
  count(*) as cnt
from source_data
where uid is not null
  and parse_url(replace(replace(url,'%3A',':'),'%2F','/'),'PROTOCOL') in ('http', 'https')
group by uid, url
),
tt as (
select
  t.uid,
  case 
    when t.url = 'cars.ru' and cnt >= 10 then 1
    when t.url = 'avto-russia.ru' and cnt >= 10 then 1
    when t.url = 'bmwclub.ru' and cnt >= 10 then 1
      else 0
  end as user_cat1_flag,
  case 
    when t.url = 'postnauka.ru' and cnt >= 10 then 1
    when t.url = 'plantarium.ru' and cnt >= 10 then 1
    when t.url = 'lensart.ru' and cnt >= 10 then 1
      else 0
  end as user_cat2_flag,
  case 
    when t.url = 'pass.rzd.ru' and cnt >= 10 then 1
    when t.url = 'rzd.ru' and cnt >= 10 then 1
    when t.url = 'vokrug.tv' and cnt >= 10 then 1
      else 0
  end as user_cat3_flag,
  case 
    when t.url = 'apteka.ru' and cnt >= 10 then 1
    when t.url = 'doctor.ufacity.info' and cnt >= 10 then 1
    when t.url = 'womanhit.ru' and cnt >= 10 then 1
      else 0
  end as user_cat4_flag
  from t)
select
  tt.uid,
  case when sum(tt.user_cat1_flag) > 0 then 1 else 0
  end as user_cat1_flag,
  case when sum(tt.user_cat2_flag) > 0 then 1 else 0
  end as user_cat2_flag,
  case when sum(tt.user_cat3_flag) > 0 then 1 else 0
  end as user_cat3_flag,
  case when sum(tt.user_cat4_flag) > 0 then 1 else 0
  end as user_cat4_flag
  from tt
  group by tt.uid
  order by tt.uid;
  
# Выгрузка данных в Hive:
Поскольку выгрузить в файл в HDFS HIVE не позволил:
rror: Error while compiling statement: FAILED: SemanticException Error creating temporary folder on: hdfs://bd-master.newprolab.com:8020/tmp/konstantin.ivanchenko/hive/lab03_result (state=42000,code=40000)
пришлось вытащить файл таблицы.

# Уточняем параметры нашей таблицы (интересует Locaton)
desc formatted lab03_users;

# Копируем файл в домашнюю директорию:
hdfs dfs -get /warehouse/tablespace/external/hive/konstantin_ivanchenko.db/lab03_users/000000_0 ~/lab03_users.txt