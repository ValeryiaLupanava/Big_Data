
## Подготовка данных в HDFS

Для начала копируем файлы в свою папку на HDFS

```shell
$ hdfs dfs -mkdir '/tmp/pavel.borisov/lab03data/'
$ hdfs dfs -cp 'labs/lab03data/' '/tmp/pavel.borisov/lab03data/'
```

Также заранее создаем папку для результата

```shell
$ hdfs dfs -mkdir '/tmp/pavel.borisov/lab03data/results/'
```

## Создание таблицы и загрузка данных


```sql
-- Проверяем, что база создана
SHOW DATABASES;

-- Переходим в нужную базу
USE pavel_borisov

-- Создаем таблицу с указанием location на папку в HDFS
CREATE EXTERNAL TABLE lab_03_puborisov
(
	uid string,
	ts float,
	url string
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'
STORED AS TEXTFILE
LOCATION '/tmp/pavel.borisov/lab03data/';
```

## Расчет флагов и сохранение в HDFS

Так как я загружал в Hive исходные данные, то и очистку и расчет флагов делаю средствами Hive

```sql
-- Вывод результатов в HDFS
INSERT OVERWRITE DIRECTORY 'hdfs://bd-master.newprolab.com:8020/tmp/pavel.borisov/lab03data/results'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
-- Приведение таблицы к требуемому виду
SELECT
    main.uid AS uid,
    nvl(cat1.user_cat1_flag,0) AS user_cat1_flag,
    nvl(cat2.user_cat2_flag,0) AS user_cat2_flag,
    nvl(cat3.user_cat3_flag,0) AS user_cat3_flag,
    nvl(cat4.user_cat4_flag,0) AS user_cat4_flag
FROM
(
	(
		(
			-- Определение всех uid с учетом очистки данных
            (
				SELECT DISTINCT uid
				FROM lab_03_puborisov
				WHERE url rlike '(^http|^https){1}(%3A|:){1}(%2F|/){2}' AND LENGTH(uid)>1
			) main
            -- Добавление 1го флага через Left Join по uid
			LEFT OUTER JOIN
			(
				SELECT uid, 1 AS user_cat1_flag
				FROM
                -- Очистка данных перед расчетом для 1го флага
				(
					SELECT uid, url, replace(parse_url(replace(replace(url, '%3A', ':'), '%2F', '/'), 'HOST'), 'www.', '') AS url_host
					FROM lab_03_puborisov
					WHERE url rlike '(^http|^https){1}(%3A|:){1}(%2F|/){2}' AND LENGTH(uid)>1
				) t
                -- Определение условий 1ой категории через 3 домена, а также посещение хотя бы одного >=10 раз
				WHERE url_host rlike 'cars.ru|avto-russia.ru|bmwclub.ru'
				GROUP BY uid, url_host
				HAVING count(*) >= 10
			) cat1
			ON (main.uid = cat1.uid)
		)
        -- Добавление 2го флага через Left Join по uid
		LEFT OUTER JOIN 
		(
			SELECT uid, 1 AS user_cat2_flag
			FROM
            -- Очистка данных перед расчетом для 2го флага
			(
				SELECT uid, url, replace(parse_url(replace(replace(url, '%3A', ':'), '%2F', '/'), 'HOST'), 'www.', '') AS url_host
				FROM lab_03_puborisov
				WHERE url rlike '(^http|^https){1}(%3A|:){1}(%2F|/){2}' AND LENGTH(uid)>1
			) t
            -- Определение условий 2ой категории через 3 домена, а также посещение хотя бы одного >=10 раз
			WHERE url_host rlike 'zakon.kz|egov.kz|makler.md'
			GROUP BY uid, url_host
			HAVING count(*) >= 10
		) cat2
		ON (main.uid = cat2.uid)
	)
    -- Добавление 3го флага через Left Join по uid
	LEFT OUTER JOIN
	(
		SELECT uid, 1 AS user_cat3_flag
		FROM
        -- Очистка данных перед расчетом для 3го флага
		(   
			SELECT uid, url, replace(parse_url(replace(replace(url, '%3A', ':'), '%2F', '/'), 'HOST'), 'www.', '') AS url_host
			FROM lab_03_puborisov
			WHERE url rlike '(^http|^https){1}(%3A|:){1}(%2F|/){2}' AND LENGTH(uid)>1
		) t
        -- Определение условий 3ой категории через 3 домена, а также посещение хотя бы одного >=10 раз
		WHERE url_host rlike 'russianfood.com|psychologies.ru|gotovim.ru'
		GROUP BY uid, url_host
		HAVING count(*) >= 10
	) cat3
	ON (main.uid = cat3.uid)
)
-- Добавление 4го флага через Left Join по uid
LEFT OUTER JOIN
(
	SELECT uid, 1 AS user_cat4_flag
	FROM
    -- Очистка данных перед расчетом для 4го флага
	(
		SELECT uid, url, replace(parse_url(replace(replace(url, '%3A', ':'), '%2F', '/'), 'HOST'), 'www.', '') AS url_host
		FROM lab_03_puborisov
		WHERE url rlike '(^http|^https){1}(%3A|:){1}(%2F|/){2}' AND LENGTH(uid)>1
	) t
    -- Определение условий 4ой категории через 3 домена, а также посещение хотя бы одного >=10 раз
	WHERE url_host rlike 'books.imhonet.ru|zhurnaly.biz|zvukobook.ru'
	GROUP BY uid, url_host
	HAVING count(*) >= 10
) cat4
ON (main.uid = cat4.uid);
```
## Сохранение результатов в целевой файл для автопроверки

```shell
$ hdfs dfs -cat /tmp/pavel.borisov/lab03data/results/* > ~/lab03_users.txt
```