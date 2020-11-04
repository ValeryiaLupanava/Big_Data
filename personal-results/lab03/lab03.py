#!/opt/anaconda/envs/bd9/bin/python

'''
hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar -D mapred.reduce.tasks=0 -input /labs/lab03data/* -output /user/valeria.lupanova/lab03/input -mapper "/opt/anaconda/envs/bd9/bin/python lab03.py" -file "./lab03.py"
'''

from urllib.parse import urlparse, unquote
import sys
import re

def url2domain(url):
    try:
        a = urlparse(unquote(url.strip()))
        if (a.scheme in ['http','https']):
            b = re.search("(?:www\.)?(.*)",a.netloc).group(1)
            if b is not None:
                return str(b).strip()
            else:
                return ''
        else:
            return ''
    except:
        return ''
    
def mapper(line):
    
    uid, ts, url = line.split('\t')
    
    if (uid is not None and url is not None and
        uid != '-' and url != '-' and #for lab03s
        (re.match(r'^http.+$', url) or re.match(r'^https.+$', url))):
        domain = url2domain(url)
        print('{}\t{}\t{}'.format(uid, ts, domain))

                    
def main():

    for line in sys.stdin:
        try:
            mapper(line)
        except ValueError:
            continue


if __name__ == '__main__':
    main()
