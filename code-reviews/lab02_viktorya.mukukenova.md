### Баш для старта hadoop

#Использовала map only


```bash
hadoop jar hadoop-streaming.jar \
-files  mapper.py \
-mapper "python3 mapper.py" \
-input /labs/lab02data/facetz_2015_02_28/ \
-output /user/lili.sabirzyanova/result
```

### mapper.py

```python
#!/opt/anaconda/envs/bd9/bin/python
#mapper

import happybase
import sys

N = 141
node = 'bd-node2.newprolab.com'
table_name = b'lili.sabirzyanova'

table = None


def do_map(key, timestamp, url):
    do_emit(key, timestamp, url)


def do_emit(key, timestamp, url):
    table = get_table()
    table.put(key, {b'data:url': url}, timestamp=timestamp)
    print(key, timestamp, url)


def main():
    for line in sys.stdin:
        s = line.split('\t')
        print (s)
        if len(s) != 3:  # validate string
            continue

        uid, timestamp, url = s
        url = url.strip()
        

        if url[0:4] != "http" or url == "-" or uid == "-":  # validate data
            continue

        
        if int(uid) % 256 != N:  # check uid
            continue

        timestamp = int(float(timestamp)*1000)
        do_map(uid, timestamp, url)
    pass


def get_table():  # Auto create table if is not exist
    global table
    if table is not None:
        return table
    connection = happybase.Connection(node, autoconnect=False)
    if table_name not in connection.tables():
        connection.create_table(table_name, {'data': dict(max_versions=4096)})
    table = connection.table(table_name)
    return table
 
main()
if __name__ == '__main__':
    main()
```    
# тоже использовала map only, reducer по сути не нужен 
# обработка нештатных значений есть
# вложенных циклов нет, это хорошо
# повторяющихся кусков кода нет, это тоже хорошо
# комментарии к коду понятны 
# есть захардкоженные значения, в идеале, вероятно, нужно параметры выносить в параметры mapper-а
# Отступы соблюдены, читабельность +++ :)
