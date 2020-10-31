-- hadoop fs -mkdir /user/mikhail.novikov/hadoop/
-- hadoop fs -cp /labs/lab03data /user/mikhail.novikov/hadoop/
-- hadoop fs -mkdir /user/mikhail.novikov/hive/
-- hadoop fs -mkdir /user/mikhail.novikov/hive/lab03_raw/
-- hadoop fs -mkdir /user/mikhail.novikov/hive/lab03_pre_out/
-- beeline jdbc:hive2://bd-node2.newprolab.com:10000 -n  name.surname -p password -f ./lab03/lab03_mikhail_novikov.sql

-- чистим таблички перед работой
drop table if exists mikhail_novikov.lab03_raw;
drop table if exists mikhail_novikov.lab03_pre_out;

-- создаем новые таблички
create external table mikhail_novikov.lab03_raw(
    uid int,
    url_timestamp float,
    url string)
    comment 'Lab03 input data'
    row format delimited
    fields terminated by '\t'
    lines terminated by '\n'
    stored as textfile
    location '/user/mikhail.novikov/hive/lab03_raw/';


create external table mikhail_novikov.lab03_users(
    uid int,
    user_cat1_flag int,
    user_cat2_flag int,
    user_cat3_flag int,
    user_cat4_flag int)
    comment 'Lab03 output data'
    row format delimited
    fields terminated by '\t'
    lines terminated by '\n'
    stored as textfile
    location '/user/mikhail.novikov/hive/lab03_users/';

-- загружаем данные в lab03_in
load data inpath '/user/mikhail.novikov/hadoop/lab03data/*' overwrite into table mikhail_novikov.lab03_raw;

-- проверяем загрузку
 select * from mikhail_novikov.lab03_raw limit 100;

-- парсим url, считаем соответсие условию групп, пишем в lab03_out
insert overwrite table mikhail_novikov.lab03_users
	select
		ttt.uid as uid,
		if(sum(user_cat1_url1_flag) >= 10 or sum(user_cat1_url2_flag) >= 10 or sum(user_cat1_url3_flag) >= 10, 1, 0) as user_cat1_flag,
		if(sum(user_cat2_url1_flag) >= 10 or sum(user_cat2_url2_flag) >= 10 or sum(user_cat2_url3_flag) >= 10, 1, 0) as user_cat2_flag,
		if(sum(user_cat3_url1_flag) >= 10 or sum(user_cat3_url2_flag) >= 10 or sum(user_cat3_url3_flag) >= 10, 1, 0) as user_cat3_flag,
		if(sum(user_cat4_url1_flag) >= 10 or sum(user_cat4_url2_flag) >= 10 or sum(user_cat4_url3_flag) >= 10, 1, 0) as user_cat4_flag
	from
		(
		select
		    tt.uid as uid,
		    tt.url_timestamp as url_timestamp,
		    tt.url as url,
		    tt.parsed_url as parsed_url,
		    if(tt.parsed_url = 'cars.ru', 1, 0) as user_cat1_url1_flag,
		    if(tt.parsed_url = 'avto-russia.ru', 1, 0) as user_cat1_url2_flag,
		    if(tt.parsed_url =  'bmwclub.ru', 1, 0) as user_cat1_url3_flag,
		    --------------------------------------------------------------------
		    if(tt.parsed_url = 'postnauka.ru', 1, 0) as user_cat2_url1_flag,
		    if(tt.parsed_url = 'plantarium.ru', 1, 0) as user_cat2_url2_flag,
		    if(tt.parsed_url = 'lensart.ru', 1, 0) as user_cat2_url3_flag,
		    --------------------------------------------------------------------
		    if(tt.parsed_url = 'pass.rzd.ru', 1, 0) as user_cat3_url1_flag,
		    if(tt.parsed_url = 'rzd.ru', 1, 0) as user_cat3_url2_flag,
		    if(tt.parsed_url = 'bmwclub.ru', 1, 0) as user_cat3_url3_flag,
		    --------------------------------------------------------------------
		    if(tt.parsed_url = 'cars.ru', 1, 0) as user_cat4_url1_flag,
		    if(tt.parsed_url = 'avto-russia.ru', 1, 0) as user_cat4_url2_flag,
		    if(tt.parsed_url = 'vokrug.tv', 1, 0) as user_cat4_url3_flag
	    from
	        (
	        select
	        t.uid as uid,
	        t.url_timestamp * 1000 as url_timestamp,
	        t.url as url,
	        parse_url(replace(replace(replace(t.url, '%3A', ':'), '%2F', '/'), 'www.', ''), 'HOST') as parsed_url
	        from
	            (
	            select
	            uid,
	            url_timestamp,
	            url
	            from mikhail_novikov.lab03_raw
	            where uid is not NULL and url is not NULL and url rlike '(^http|^https){1}(%3A|:){1}(%2F|/){2}'
	            ) t
	        ) tt
	   ) ttt
	group by uid
	order by uid asc;

-- проверяем табличку
 select * from mikhail_novikov.lab03_users limit 100;

-- крайний селект на выгрузку из базы согласно условиям задания
insert overwrite directory 'hdfs://bd-master.newprolab.com:8020/user/mikhail.novikov/lab03result/'
    row format delimited
    fields terminated by ','
    stored as textfile

    select
		uid,
		user_cat1_flag,
		user_cat2_flag,
		user_cat3_flag,
		user_cat4_flag
    from mikhail_novikov.lab03_users
    order by uid
   	limit 200;

-- чистим таблички после себя
drop table if exists mikhail_novikov.lab03_raw;
drop table if exists mikhail_novikov.lab03_users;

-- смотрим наш result файлик
-- hadoop fs -ls /user/mikhail.novikov/lab03result
-- hadoop fs -cat /user/mikhail.novikov/lab03result/* | tr ',' '\t' > ~/lab03_users.txt

-- чистим за собой
-- hadoop fs -rm -r /user/mikhail.novikov/hadoop/
-- hadoop fs -rm -r /user/mikhail.novikov/hive/
-- hadoop fs -rm -r /user/mikhail.novikov/lab03result/*
-- hadoop fs -rm -r /user/mikhail.novikov/.Trash
