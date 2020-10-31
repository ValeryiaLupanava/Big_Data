#!/opt/anaconda/envs/bd9/bin/python

import sys
import happybase

#Привет (:
#Можно указать строку запуска файла

def emit(uid, timestamp, url):
    connection = happybase.Connection('bd-node2.newprolab.com')
    table = connection.table('ekaterina.kucheryavenko')
    print('Create table')

    #Переменные обычно не называют системными именами,наприме, timestamp.
    #Сокращение hb не совсем понятно
    hb = table.batch(timestamp=int(float(timestamp)*1000))
    #Преобразование timestamp нужно вынести в переменную.
    url = url.strip()

    try:
        hb.put(uid, {'data:url': url})
    except ValueError as e: 
    #Можно записать ошибку, а не просто скипнуть.
    #Потом анализировать гэпы проще.
        pass
    else:
        hb.send()

#Эту часть нужно обернуть в функцию, чтобы можно было отдельно блок запускать и тестировать.
for line in sys.stdin:
    try:
        uid, ts, url = line.strip().split('\t')
    except ValueError:
    #Опять же, ошибку можно записать.
    #Я бы эксепшен поместила после блока if, чтобы if также попадал в обработку.
        continue
    if len(uid)>3 and url.lower().startswith('http')is True and int(uid) % 256 == 173:
        #Нужна дополнительная проверка timestamp, чтобы убедиться, что это число,
        #потому что потом идет преобразование.
        print('Find!')
        emit(uid, ts, url)
#Нет закрытия коннекшена close().
        
#Для отладки кода лучше применять функцию __name__==__main__.
#Это позволит исполнять не весь код файла, а тот, что будет указан в функции main().
#Удобно для отладки кода и прослеживания логики исполнения.
#Например:
#def main():
#   something
#if __name__ == '__main__':
#   main()

#Еще нужно было бы комментарии в коде добавить, 
#чтобы смысл был понятен каждому, открывшему файл.
#Но я у себя тоже забыла описать (:

#Хороших выходных! (:
