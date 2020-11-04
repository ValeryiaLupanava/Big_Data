-- создать таблицу с исходными данными
CREATE EXTERNAL TABLE IF NOT EXISTS lab03 
( UID bigint
 ,time_stamp float
 ,URL String
)
COMMENT 'table for lab03'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'
STORED AS TEXTFILE;

-- загрузить данные в исходную таблицу
LOAD DATA INPATH '/tmp/avertyagin/lab03/lab03data/' OVERWRITE INTO TABLE lab03;

-- временная таблица с UID из 12 сайтов	 
CREATE TEMPORARY TABLE tmp_lab3_12s AS  --## не понятно обозначение таблицы, первичный ключ задан, AS излишне
SELECT 
  UID
 ,SUM(
    CASE
      WHEN host = 'cars.ru' THEN 1 ELSE 0
    END) cnt_cars
 ,SUM(
    CASE
      WHEN host = 'avto-russia.ru' THEN 1 ELSE 0
    END) cnt_avto
 ,SUM(
    CASE
      WHEN host = 'bmwclub.ru' THEN 1 ELSE 0
    END) cnt_bmwclub
 ,SUM(
    CASE
      WHEN host = 'fastpic.ru' THEN 1 ELSE 0
    END) cnt_fastpic
 ,SUM(
    CASE
      WHEN host = 'fotoshkola.net' THEN 1 ELSE 0
    END) cnt_fotoshkola
 ,SUM(
    CASE
      WHEN host = 'bigpicture.ru' THEN 1 ELSE 0
    END) cnt_bigpicture
 ,SUM(
    CASE
      WHEN host = 'nirvana.fm' THEN 1 ELSE 0
    END) cnt_nirvana
 ,SUM(
    CASE
      WHEN host = 'rusradio.ru' THEN 1 ELSE 0
    END) cnt_rusradio
 ,SUM(
    CASE
      WHEN host = 'pop-music.ru' THEN 1 ELSE 0
    END) cnt_music
 ,SUM(
    CASE
      WHEN host = 'snowmobile.ru' THEN 1 ELSE 0
    END) cnt_snowmobile
 ,SUM(
    CASE
      WHEN host = 'nastroisam.ru' THEN 1 ELSE 0
    END) cnt_nastroisam
 ,SUM(
    CASE
      WHEN host = 'mobyware.ru' THEN 1 ELSE 0
    END) cnt_mobyware	
--## очень неоднозначный стиль, вроде и структура удобная, но глазу не нравится...
FROM 
  (SELECT 
     UID
    ,REPLACE(PARSE_URL( REPLACE( REPLACE(URL, '%3A', ':'), '%2F', '/'), 'HOST'), 'www.', '') as host
   FROM lab03
   WHERE 
     UID IS NOT NULL AND ( SUBSTR(URL, 1, 13) = 'http%3A%2F%2F' OR SUBSTR(URL, 1, 14) = 'https%3A%2F%2F' )   
   --## там было несколько url не удволетворяющих этому условию, через URL rlike '(^http|^https){1}(%3A|:){1}(%2F|/){2}'  былобы лучше
   ) AS t 
GROUP BY 
  UID;
	 
-- результирующая таблица с 4 категориями
CREATE TEMPORARY TABLE tmp_lab3_res AS  --## AS
--## для аччивки она понадобилась, можно было сохранить как external
SELECT 
   UID
  ,CASE
     WHEN cnt_cars >= 10 OR cnt_avto >= 10 OR cnt_bmwclub >= 10 THEN 1 ELSE 0
   END as cat1
  ,CASE
     WHEN cnt_fastpic >= 10 OR cnt_fotoshkola >= 10 OR cnt_bigpicture >= 10 THEN 1 ELSE 0
   END as cat2
  ,CASE
     WHEN cnt_nirvana >= 10 OR cnt_rusradio >= 10 OR cnt_music >= 10 THEN 1 ELSE 0
   END as cat3
  ,CASE
     WHEN cnt_snowmobile >= 10 OR cnt_nastroisam >= 10 OR cnt_mobyware >= 10 THEN 1 ELSE 0
   END as cat4  
FROM tmp_lab3_12s
ORDER BY UID;


INSERT OVERWRITE DIRECTORY 'hdfs://bd-master.newprolab.com:8020/user/alexander.vertyagin/lab03/lab03result'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
SELECT *
FROM tmp_lab3_res;
--## можно использовать limit 200 чтобы выгрузить только нужные 200 строк в файлик.

hdfs dfs -cat /user/alexander.vertyagin/lab03/lab03result/* > ~/lab03_users.txt   --## круто, кластер не резиновый, а за собой почистить после?
