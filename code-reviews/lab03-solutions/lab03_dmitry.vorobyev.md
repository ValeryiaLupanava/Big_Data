# Основная лаба
Для очистки данных использовал скрипт с приложенной в задании функцией

`cleaner.py:`
```python
import sys
from urllib.parse import urlparse, unquote
import re

def emit(uid, url):
    sys.stdout.write('{}\t{}\n'.format(uid, url))

# this file extracts url from input strings
def url2domain(url):
    try:
        a = urlparse(unquote(url.strip()))
        if a.scheme in ['http', 'https']:
            b = re.search("(?:www\.)?(.*)", a.netloc).group(1)
            if b is not None:
                return str(b).strip()
            else:
                return ''
        else:
            return ''
    except:
        return None


def get_record_from_line(line):
    splitted_line = line.strip().split("\t")
    if len(splitted_line) != 3:
        return None
    (uid, timestamp, url) = splitted_line
    # validate parts of line
    if uid is None or len(uid) < 3 or str(uid).isdigit() is False:
        return None
    if url is None or len(url) < 3 or url2domain(url) is None:
        return None
    # convert data and return
    url = url2domain(url)
    return uid, timestamp, url


def main():
    for line in sys.stdin.readlines():
        record = get_record_from_line(line)
        if record is None:
            continue
        (uid, timestamp, url) = record
        emit(uid, url)


if __name__ == '__main__':
    main()

```

Создал табличку в хайве:
```hiveql
create external table dmitry_vorobyev (
    uid bigint,
    url varchar(1000)
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'
LOCATION '/user/dmitry.vorobyev/dmitry_vorobyev/';
```

Затем загрузил туда таблицу, пропустив исходные данные через скрипт cleaner.py. MR-джобу не делал, данных не так много было
```
hadoop fs -cat /labs/lab03data/* | python3 cleaner.py |  hadoop fs -put - /user/dmitry.vorobyev/dmitry_vorobyev/00000_0.txt
```

Затем выполнил такой запрос:
```hiveql
with user_info as (
    select
    t.uid as uid,
    CASE WHEN t.url in ('cars.ru', 'avto-russia.ru', 'bmwclub.ru') then 1 else 0 END as is_auto,
    CASE WHEN t.url in ('fastpic.ru', 'fotoshkola.net', 'bigpicture.ru') then 1 else 0 END as is_design,
    CASE WHEN t.url in ('nirvana.fm', 'rusradio.ru', 'pop-music.ru') then 1 else 0 END as is_music,
    CASE WHEN t.url in ('snowmobile.ru', 'nastroisam.ru', 'mobyware.ru') then 1 else 0 END as is_gadget
    from dmitry_vorobyev t
)

INSERT OVERWRITE DIRECTORY 'hdfs://bd-master.newprolab.com:8020/user/dmitry.vorobyev/lab03result'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE

select
    u1.uid,
    CASE WHEN sum(u1.is_auto) >= 10 then 1 else 0 END as user_cat1_flag,
    CASE WHEN sum(u1.is_design) >= 10 then 1 else 0 END as user_cat2_flag,
    CASE WHEN sum(u1.is_music) >= 10 then 1 else 0 END as user_cat3_flag,
    CASE WHEN sum(u1.is_gadget) >= 10 then 1 else 0 END as user_cat4_flag
from user_info u1
GROUP BY  u1.uid
ORDER BY 1
```