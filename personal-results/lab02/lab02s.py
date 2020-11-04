#!/opt/anaconda/envs/bd9/bin/python
"""mapper+reducer"""

'''
hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar -D mapred.reduce.tasks=0 -input /labs/lab02data/facetz_2015_02_12/* -output /user/valeria.lupanova/results -mapper "/opt/anaconda/envs/bd9/bin/python lab02s.py" -file "./lab02s.py"
'''

import happybase
import sys
import re
import fileinput
import os
from decimal import Decimal
import collections
from datetime import datetime

def mapper(line, urls):
    uid, ts, url = line.split('\t')    
    if re.match(r'^[\d]+$', (uid.split('\t'))[0]):
        if url and url.strip():
            urls.append(url)


def main():
    urls = []  
    top_350 =[]
    top_N = 350

    for line in sys.stdin:
        mapper(line, urls)
        
    occurrences = collections.Counter(urls)
    for url, count in occurrences.most_common(top_N):
            top_350.append([url, count])
            
    occurrences = collections.Counter(urls)
    for url, count in occurrences.most_common(top_N):
        print('{}\t{}\n'.format(url,count))

    
if __name__ == '__main__':
    main()
