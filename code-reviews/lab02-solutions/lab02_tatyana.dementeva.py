#!/opt/anaconda/envs/bd9/bin/python
import happybase
connection = happybase.Connection('bd-node2.newprolab.com')
table = connection.table("tatyana.dementeva")

import sys

def map(line):
        if len(line.strip().split("\t"))==3:
            UID, timestamp, URL = line.strip().split("\t")
            try:
                uid = int(UID)
            except ValueError:
                uid = UID
            try:
                ts = float(timestamp)
            except ValueError:
                ts = timestamp
            if type(uid)==int and type(ts)==float and URL[:4]=='http' and uid % 256 == 98:
                table.put(str(uid), {b'data:url':URL}, timestamp=int(ts*1000))

def main():
        for line in sys.stdin:
                map(line)

if __name__ == '__main__':
        main()
