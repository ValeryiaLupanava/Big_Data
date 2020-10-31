#!/opt/anaconda/envs/bd9/bin/python
import happybase
import sys

connection = happybase.Connection('spark-master.newprolab.com')
connection.open()
table_name='alexander.pavlyuk'
table = connection.table(table_name)

#именование параметров делаем маленькими буквами
def write_to_base (table_name, UID, time_stamp, URL):
    #непонятно в чем смысл переменной value_name, почему нельзя сразу передать url
    value_name='{}'.format(URL)
    #uid  и так string, лишнее приведение
    row_key=str(UID)
    table.put(row_key, {b"data:url":value_name}, timestamp=time_stamp)

def map(line):
    objects = line.split('\t')
    if len(objects) ==3:
        #именование переменных делаем маленькими буквами
        UID, time_stamp, URL = objects
        #непонятно для чего тут это приведение а через 3 строчки мы сравниваем time_stamp со стрингом
        time_stamp=float(time_stamp)
        #а почему https отсекается? в условии сказано: URL должны начинаться с http
        #я бы разместил все 3 условия на одной строчке через and
        if "https" not in URL:
            if UID!= "-" and time_stamp != "-":
                #зачем uid приводится к float а не int?
                if float(UID)%256 == 65:
                    time_stamp=int(time_stamp*1000)
                    #мне кажется правильней будет приведение time_stamp сделать сразу аргументом функции, а не отдельной строкой
                    #write_to_base(table_name, UID, int(float(time_stamp)*1000) , URL)
                    write_to_base(table_name, UID, time_stamp, URL)
                    
def mapper():
       for line in sys.stdin:
               map(line.strip())
    #забыл закрыть соединение           
    #connnection.close()               

if __name__=='__main__':
    mapper()
