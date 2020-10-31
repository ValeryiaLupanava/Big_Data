# Решение лабораторной работы #2

## Состав

Решение состоит из файла маппера и файла запуска. 
Необходимая таблица создаётся автоматически при необходимости.

## Маппер

```python
#!/opt/anaconda/envs/bd9/bin/python

USERNAME="semen.bochkarev"
N=141

import sys

import happybase

connection = happybase.Connection('bd-node2.newprolab.com')

try:
  connection.create_table(
      USERNAME,
      {
       'data': dict(max_versions=4096),
      }
  )
except Exception as e:
  pass
  
table = connection.table(USERNAME)

def mapper(line):
    line = line.strip()
    try:
        uid, timestamp, url = line.split('\t')
    except:
        return None
    if uid.isdigit() and url.startswith('http'):
        uid = int(uid)
        timestamp = int(float(timestamp) * 1000)
        if uid % 256 == N:
            table.put(str(uid), {b'data:url': str.encode(url)}, timestamp=timestamp)
    return url

for line in sys.stdin:
    mapper(line)
```

## Скрипт запуска

```bash
#!/bin/bash

hadoop fs  -rm -R -skipTrash /user/semen.bochkarev/lab02

hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar \
    -D mapred.reduce.tasks=0 \
    -file ./mapper.py    -mapper ./mapper.py \
    -input /labs/lab02data/facetz_2015_02_06/* \
    -output /user/semen.bochkarev/lab02
```
