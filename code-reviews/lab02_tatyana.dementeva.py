import sys
import happybase


# emit data to hbase
def emit_to_hbase(uid, timestamp, url):
    connection = happybase.Connection('bd-node2.newprolab.com')
    table = connection.table('dmitry.vorobyev')
    table.put(uid, {'data:url': url}, timestamp)
    # better solution is to open the connection, put data and then close the connection,
    # but for the sake of code simplicity for the lab we open and close connection within the method
    connection.close()


# returns tuple of (uid: string, timestamp: int, url: string), or None if line could not be parsed
def get_record_from_line(line):
    splitted_line = line.strip().split("\t")
    if len(splitted_line) != 3:
        return None
    (uid, timestamp, url) = splitted_line
    # validate parts of line
    # Не очень понятно, с какой целью делается проверка на длину переменных - кажется такого условия в задаче нет
    # Выражения типа result is False можно заменить на not result
    if uid is None or len(uid) < 3 or str(uid).isdigit() is False:
        return None
    if timestamp is None or len(timestamp) < 5 or is_float(timestamp) is False:
        return None
    if url is None or len(url) < 10 or str(url).lower().startswith('http') is False:
        return None
    # check mod by task
    # Возможно 178 стоит вынести в константу, чтобы избежать хардкода
    if int(uid) % 256 != 178:
        return None
    # convert data and return
    timestamp = int(float(timestamp) * 1000)
    return uid, timestamp, url


# check if the input string is floating point number
def is_float(arg):
    try:
        float(arg)
        return True
    except ValueError:
        return False


def main():
    for line in sys.stdin.readlines():
        record = get_record_from_line(line)
        if record is None:
            continue
        (uid, timestamp, url) = record
        emit_to_hbase(uid, timestamp, url)


if __name__ == '__main__':
    main()
