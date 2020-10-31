#!/opt/anaconda/envs/bd9/bin/python
import happybase
# соединение открывается, но нигде не закрывается в коде
connection = happybase.Connection('bd-node2.newprolab.com')
table = connection.table("tatyana.dementeva")

# обычно импорты идут скопом вначале файла
import sys

# слишком большие отступы в функциях
def map(line):
        # некритично, но отсутствуют пробелы, затрудняет чтение, (line.strip().split("\t")) == 3:
        if len(line.strip().split("\t"))==3:
            # названия переменных в функции должны быть с маленькой буквы
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
