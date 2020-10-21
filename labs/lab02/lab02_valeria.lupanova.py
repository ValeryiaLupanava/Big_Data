#!/opt/anaconda/envs/bd9/bin/python
"""mapper+reducer"""

'''
hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar -D mapred.reduce.tasks=0 -input /labs/lab02data/facetz_2015_02_12/* -output /user/valeria.lupanova/results -mapper "/opt/anaconda/envs/bd9/bin/python lab02.py" -file "./lab02.py"
'''

import happybase
import sys
import re


def mapper(line):
    uid, ts, url = line.split('\t')
    if re.match(r'^[\d]+$', (uid.split('\t'))[0]):
        if re.match(r'^[\d]+\.[\d]+$', ts):
            if re.match(r'^http.+$', url):
                if int(uid)%256==157:
                    ts = int(float(ts)*1000)
                    reducer(uid, ts, url)

                    
def reducer(uid, ts, url):
    connection = happybase.Connection('bd-node2.newprolab.com')
    connection.open()
    table = connection.table('valeria.lupanova')
    try:
        table.put(row=str(uid), data={b'data:url':url}, timestamp=ts)
    except:
        print('Error!')
    else:
        print('Success!')
    finally:
        connection.close()
                

def main():
    for line in sys.stdin:
        mapper(line)


if __name__ == '__main__':
    main()
