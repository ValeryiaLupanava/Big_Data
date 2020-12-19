## AB: мои комментарии.
#!/opt/anaconda/envs/bd9/bin/python

# mapper-only job
# ниже представлен код mapper.py

import happybase
import sys

N = 157
TABLE_NAME = 'alexander.alexandrov'
HOST = 'bd-node2.newprolab.com'

table = None

def emit(uid, timestamp, http):
    if table is not None:
        sys.stdout.write('sdf')
        table.put(uid, {b'data:url': http}, timestamp=timestamp)
    else:
        sys.stdout.write('{}\t{}\t{}\n'.format(uid, timestamp, http))
        
def do_map(line):
    objects = line.split('\t')
    if len(objects) == 3:
        uid, timestamp, http = objects[0], int(float(objects[1]) * 1000), objects[2] 
        if int(uid) % 256 == N and http.startswith('http'):
            emit(uid, timestamp, http)
## AB: По идее все проверки можно делать в рамках одного оператора IF если сразу обращать строку в list.
## objects = list(line.split('\t'))
##    if len(l) == 3 and l[2].startswith('http') and int(l[0]) % 256 == N:
## Но это не обязательно.
## Нужна вроде проверка, что в uid не лежит прочерк - хотя в таком случае, наверное, сработает except ValueError из main.

def main():
    connection = happybase.Connection(HOST)
    global table
    table = connection.table(TABLE_NAME)
    for line in sys.stdin:
        try:
            do_map(line.strip())
        except ValueError:
            continue
    connection.close()

if __name__ == '__main__':
    main()

    
## AB:Даже не знаю что и добавить:) Виден опыт работы в разработке, учтены кейсы возможных Data Quality issues - проверка на наличие 
## таблицы, обработка ошибок в случае некорректных данных в строке - всё есть. 

