#!/opt/anaconda/envs/bd9/bin/python

import sys
import happybase

def emit_to_sys(uid, timestamp, url):
    sys.stdout.write('{}\t{}\t{}\n'.format(uid, timestamp, url))

def emit_to_hbase (uid,timestamp,url):
    try:
        connection = happybase.Connection('bd-node2.newprolab.com')
        table = connection.table('alexander.bobr')
        table.put(uid, {'data:url'.encode('utf-8'):url}, timestamp=int(float(timestamp)*1000))
        sys.stdout.write('{}\t{}\t{}\n'.format(uid, timestamp, url))
        connection.close()
    except  ValueError as e:
        sys.stdout.write(e)
    
def map(line):
    l = list(line.split('\t'))
    if len(l) == 3 and len(l[0]) > 5 and len(l[1])>5 and len(l[2]) > 5 and l[2].startswith('http'):
        if int(l[0]) % 256 == 26:
            uid = l[0]
            timestamp = l[1]
            url = l[2]
            emit_to_hbase(uid, timestamp, url)
            
def main():
    for line in sys.stdin:
        map(line.strip())
        
if __name__ == '__main__':
    main()


