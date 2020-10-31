#!/opt/anaconda/envs/bd9/bin/python
#!/usr/bin/python3 # нужна ли эта директива, если есть верхняя? Укажывает ли верхняя на окружение с Python3?


import sys
import happybase

connection = happybase.Connection('bd-node2.newprolab.com')
table = connection.table('semen.shafronov')

    
def map(line):
    objects = i.split('\t')
    if len(objects) != 3:
        return
    uid, timestamp, url = objects
    if len(uid) < 11:
        return
    if int(uid) % 256 != 25:
        return
    if url.startswith('http'):
        timestamp = int(float(timestamp) * 1000)
        sys.stdout.write('{}\t{}\t{}\n'.format(uid, timestamp, url))
        table.put(uid, {'data:url': url}, timestamp)

def main():
    for line in sys.stdin:
        map(line.strip())
        
if __name__ == '__main__': # не знаю, зачем запускаю этот запрос. Можно ли сразу запустить цикл с for line in sys.stdin...?
    main()
