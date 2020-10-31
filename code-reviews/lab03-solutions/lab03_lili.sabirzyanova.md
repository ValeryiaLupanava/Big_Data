### Лаба 03

Для начала запустила MapReduce только с маппером для фильтрации url со следующем кодом

```python
#!/opt/anaconda/envs/bd9/bin/python
#mapper

import sys

def url2domain(url):
    try:
        a = urlparse(unquote(url.strip()))
        if (a.scheme in ['http', 'https']):
            b = re.search("(?:www\.)?(.*)", a.netloc).group(1)
            if b is not None:
                return str(b).strip()
            else:
                return ''
        else:
            return ''
    except:
        return ''

def do_map(key, url):
    do_emit(key, url)


def do_emit(key, url):
    print(key, url)


def main():
    for line in sys.stdin:
    s = line.split("\t")
    if len(s) != 3:
        continue
    uid, timestamp, url = s
    url = url.strip()
    url = url2domain(url)
    if len(url) == 0:
        continue
    if uid == "-" or len(uid.strip())==0:
        continue
    do_map(uid, url)
    return table
 
main()
if __name__ == '__main__':
    main()
```


Полученный файл кладу в /tmp/lili.sabirzyanova/lab03/lab03data
Затем создаю таблицу и подключаю файл с исходными данными

```sql
CREATE EXTERNAL TABLE lili_data(
  `uid` STRING,
  `url` STRING
)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY '\t'
stored as textfile
LOCATION '/tmp/lili.sabirzyanova/lab03/lab03data'
```
Все следующие запросы можно было сделать через view и один запрос, однако, решила делать по шагово для наглядности, а так же возможности проверить какждый шаг

Создам таблицу в которой с аггрегирую и отфлиьтрую пары юзер + домен.
```sql
CREATE TABLE lili_mid as SELECT `uid`, `url`, COUNT(1) AS `scount`
FROM lili_data
GROUP BY `uid`, `url`
HAVING COUNT(1)>=10;
```

Создам таблицу с уникальным списком пользователей
```sql
CREATE lili_users AS 
SELECT `uid` FROM lili_sabirzyanova GROUP BY `uid`;
```
Финальный запрос который даст таблицу с решением задачи
```sql
CREATE EXTERNAL TABLE lili_result AS 
SELECT `uid`, 
coalesce((SELECT 1 FROM lili_sabirzyanova_mid WHERE lili_mid.`uid` = lili_users.`uid` AND `url` IN ('cars.ru', 'avto-russia.ru', 'bmwclub.ru')),0) AS `cat1`, 
coalesce((SELECT 1 FROM lili_sabirzyanova_mid WHERE lili_mid.`uid` = lili_users.`uid` AND `url` IN ('zakon.kz', 'egov.kz', 'makler.md')),0) AS `cat2,` 
coalesce((SELECT 1 FROM lili_sabirzyanova_mid WHERE lili_mid.`uid` = lili_users.`uid` AND `url` IN ('russianfood.com', 'psychologies.ru', 'gotovim.ru')),0) AS `cat3`, 
coalesce((SELECT 1 FROM lili_sabirzyanova_mid WHERE lili_mid.`uid` = lili_users.`uid` AND `url` IN ('books.imhonet.ru', 'zhurnaly.biz', 'zvukobook.ru')),0) as `cat4 `
FROM  lili_users ORDER BY CAST(`uid` AS bigint);
```
Осталось получить результат работы в виде файла

```sql
INSERT OVERWRITE DIRECTORY 'hdfs://bd-master.newprolab.com:8020/tmp/lili.sabirzyanova/lab03result'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
SELECT * from lili_result
ORDER BY `uid`;
```

Теперь остается только скачать файл с HDFS и отдать его на проверку скрипту.