-- Тут все хорошо. Возможно, вместо создания отдельной таблицы для каждой категории, можно было рассегментировать всех клиентов в одной таблице. 
-- Но, думаю, существенной роли не играет.

-- Запуск обработки на кластере необходимого файла с данными с посещением сайтов пользователями
-- yarn jar ~/hadoop-streaming.jar -input /labs/lab03data/* -output /user/ekaterina.kucheryavenko/lab_03 -file ~/lab_03/mapper.py -mapper "python3 mapper.py"

-- Создание необходимой таблицы из выхода mapreduce по посещениям сайтов
-- Если приходится перезаписывать, то делаем проверку на существующую таблицу
create external table if not exists ekucheryavenko.ekaterina_kucheryavenko
(
uid string,
url string
)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY '\t'
location '/user/ekaterina.kucheryavenko/lab_03/';


-- Создание таблицы необходимой по заданию
drop table if exists lab03_users;
create external table if not exists lab03_users
(
uid string,
user_cat1_flag string,
user_cat2_flag string,
user_cat3_flag string,
user_cat4_flag string
)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY '\t'
location '/user/ekaterina.kucheryavenko/lab03_users/';

--Чтобы несколько файлов были помещены в 1
set hive.merge.tezfiles=true;
set hive.merge.mapfiles=true;
set hive.merge.mapredfiles=true;
set hive.merge.size.per.task=128000000;
set hive.merge.smallfiles.avgsize=128000000;

with
--выделение пользователей, кто заходил на один из сайтов более 10 раз
--'cars.ru', 'avto-russia.ru', 'bmwclub.ru'
gr_1 as
(select uid, url, count(url) as cnt, 1 type_1 from ekaterina_kucheryavenko
where url in ('cars.ru', 'avto-russia.ru', 'bmwclub.ru')
group by uid, url
having count(url)>=10),
--выделение уникальных пользователей из gr_1
gr_1_cl as
(select distinct uid, type_1 from gr_1),
--выделение пользователей, кто заходил на один из сайтов более 10 раз
--'samara-papa.ru', 'vodvore.net', 'mama51.ru'
gr_2 as
(select uid, url, count(url) as cnt, 1 type_2 from ekaterina_kucheryavenko
where url in ('samara-papa.ru', 'vodvore.net', 'mama51.ru')
group by uid, url
having count(url)>=10),
--выделение уникальных пользователей из gr_2
gr_2_cl as
(select distinct uid, type_2 from gr_2),
--выделение пользователей, кто заходил на один из сайтов более 10 раз
--'sp.krasmama.ru', 'forum.krasmama.ru', 'forum.omskmama.ru'
gr_3 as
(select uid, url, count(url) as cnt, 1 type_3 from ekaterina_kucheryavenko
where url in ('sp.krasmama.ru', 'forum.krasmama.ru', 'forum.omskmama.ru')
group by uid, url
having count(url)>=10),
--выделение уникальных пользователей из gr_3
gr_3_cl as
(select distinct uid, type_3 from gr_3),
--выделение пользователей, кто заходил на один из сайтов более 10 раз
--'novayagazeta.ru', 'echo.msk.ru', 'inosmi.ru'
gr_4 as
(select uid, url, count(url) as cnt, 1 type_4 from ekaterina_kucheryavenko
where url in ('novayagazeta.ru', 'echo.msk.ru', 'inosmi.ru')
group by uid, url
having count(url)>=10),
--выделение уникальных пользователей из gr_4
gr_4_cl as
(select distinct uid, type_4 from gr_4),
--выделение уникальных пользователей во всей выборке
all_cl as
(select distinct uid from ekaterina_kucheryavenko),
--Формирование итоговой таблицы с подтягиванием информации к uid с типом группы
result as
(select all_cl.uid, type_1, type_2, type_3, type_4 from all_cl 
left join gr_1_cl on all_cl.uid=gr_1_cl.uid
left join gr_2_cl on all_cl.uid=gr_2_cl.uid
left join gr_3_cl on all_cl.uid=gr_3_cl.uid
left join gr_4_cl on all_cl.uid=gr_4_cl.uid)
--перезапись таблицы в случае уже существующих записей
INSERT OVERWRITE table lab03_users
select uid, if(type_1 is NULL, 0, type_1) as user_cat1_flag, if(type_2 is NULL, 0, type_2) as user_cat2_flag, 
if(type_3 is NULL, 0, type_3) as user_cat3_flag, if(type_4 is NULL, 0, type_4) as user_cat4_flag from result
sort by uid;
