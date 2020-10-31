## bash run script ----------------------------------------

#!/usr/bin/env sh

hadoop fs -rm -r -f result

hadoop jar ~/hadoop-streaming.jar \
        -input /labs/lab02data/facetz_2015_02_27/* \
        -output result \
        -file ~/lab_02/lab2_m.py \
        -mapper "lab2_m.py" \
        -file ~/lab_02/lab2_r.py \
        -reducer "lab2_r.py"
        
## mapper ----------------------------------------
#!/opt/anaconda/envs/bd9/bin/python
import sys

N = 226


def do_map(key, value1, value2):
    do_emit(key, value1, value2)


def do_emit(key, value1, value2):
    sys.stdout.write('{0}\t{1}\t{2}\n'.format(key, value1, value2))


def main():  # Mapper
    for line in sys.stdin:
        try:
            uid, timestamp, url = line.strip('\n').split('\t', 2)
        except ValueError:
            # logging warn: Could not split the lines
            continue
        uid = uid.strip()
        timestamp = timestamp.strip()
        url = url.strip()

        if uid.isdigit() and timestamp and url != "-" and url[:4] == 'http' and int(uid) % 256 == N:
            do_map(uid, timestamp, url)
        else:
            continue


if __name__ == '__main__':
    main()
## reducer ----------------------------------------
#!/opt/anaconda/envs/bd9/bin/python
import happybase
import sys

connection = happybase.Connection('bd-node2.newprolab.com')
# connection.open()
table_name = "mikhail.novikov"
table = connection.table(table_name)


def reduce(uid, timestamp, url):
    timestamp = int(float(timestamp) * 1000)
    emit(uid, timestamp, url)


def emit(uid, timestamp, url):
    try:
        table.put(str(uid), {'data:url': url}, timestamp=timestamp)
    except Exception as e:
        print(e)


def main():  # Reducer
    for line in sys.stdin:
        uid, timestamp, url = line.strip('\n').split('\t')
        reduce(uid, timestamp, url)


if __name__ == '__main__':
    main()
