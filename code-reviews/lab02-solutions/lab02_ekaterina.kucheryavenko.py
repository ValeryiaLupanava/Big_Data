#!/opt/anaconda/envs/bd9/bin/python

import sys
import happybase

def emit(uid, timestamp, url):
    connection = happybase.Connection('bd-node2.newprolab.com')
    table = connection.table('ekaterina.kucheryavenko')
    print('Create table')

    hb = table.batch(timestamp=int(float(timestamp)*1000))
    url = url.strip()

    try:
        hb.put(uid, {'data:url': url})
    except ValueError as e: 
        pass
    else:
        hb.send()

for line in sys.stdin:
    try:
        uid, ts, url = line.strip().split('\t')
    except ValueError:
        continue
    if len(uid)>3 and url.lower().startswith('http')is True and int(uid) % 256 == 173:
        print('Find!')
        emit(uid, ts, url)
