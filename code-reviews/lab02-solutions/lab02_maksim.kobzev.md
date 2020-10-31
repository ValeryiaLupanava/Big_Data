
### КОМАНДЫ В КОНСОЛИ


```python
#подключиться к bd-master

$ ssh -i ./newprolab.pem maksim.kobzev@bd-master.newprolab.com

#убедиться, что таблицы не существует (если существует - делаем disable, потом drop и создаем заново) и создать новую

$ echo 'describe "maksim.kobzev"' | hbase shell -n
$ echo "create 'maksim.kobzev', {NAME => ‘data’, VERSIONS => 4096}" | hbase shell -n

#создать фалы mapper.py и reducer.py в домашней директории (у меня это была './test') и сделать их исполняемыми (код для обоих файлов ниже)
$ nano ./test/mapper.py #скопировать и вставить код из блока mapper ниже
$ nano ./test/reducer.py #скопировать и вставить код из блока reducer ниже
$ chmod +x ./test/mapper.py
$ chmod +x ./test/reducer.py

#запустить MR job. Важно помнить, что аргумент -file принимает путь к файлам относительно домашней директории а не на хадупе!
hadoop jar ~/hadoop-streaming.jar -D mapred.reduce.tasks=1 -input /labs/lab02data/facetz_2015_02_15/part* -output /tmp/maksim.kobzev/r12/ -file ./test/mapper.py -file ./test/reducer.py -mapper "./mapper.py" -reducer "./reducer.py"
```

### MAPPER


```python
#mapper - сохранить этот блок в отдельный файл с названием mapper.py
#принимаем на стандартный вход содержимое файлов из директории-источника и результат выводим построчно на стандартный выход
#!/opt/anaconda/envs/bd9/bin/python
import sys
for line in sys.stdin:
    if len(line.strip().split('\t')) != 3\
    or line.strip().split('\t')[0] == '-'\
    or int(line.strip().split('\t')[0]) % 256 != 42\
    or line.strip().split('\t')[2][:4] != 'http':
        continue
    print(line.strip().split('\t')[0] + '\t' +\
          str(int(float(line.strip().split('\t')[1])*1000)) + '\t' +\
          line.strip().split('\t')[2])
```

### REDUCER


```python
#reducer - сохранить этот блок в отдельный файл с названием reducer.py
#принимаем на вход строки с uid, url и timestamp и заливаем построчно в hbase, используя библиотеку happybase
#!/opt/anaconda/envs/bd9/bin/python
import sys
import happybase
connection = happybase.Connection('bd-node2.newprolab.com')
table = connection.table(b'maksim.kobzev')

for line in sys.stdin:
    table.put(line.strip().split('\t')[0],\
              {b'data:url': str(line.strip().split('\t')[2])},\
              timestamp=int(line.strip().split('\t')[1]))
connection.close()
```
