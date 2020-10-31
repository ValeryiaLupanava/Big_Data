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
