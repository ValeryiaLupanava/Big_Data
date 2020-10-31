#!/opt/anaconda/envs/bd9/bin/python

# mapper-only job
# ниже представлен код mapper.py

import happybase
import sys

N = 157
TABLE_NAME = 'alexander.alexandrov'
HOST = 'bd-node2.newprolab.com'

table = None

def emit(uid, timestamp, http):
    if table is not None:
        sys.stdout.write('sdf')
        table.put(uid, {b'data:url': http}, timestamp=timestamp)
    else:
        sys.stdout.write('{}\t{}\t{}\n'.format(uid, timestamp, http))
    
def do_map(line):
    objects = line.split('\t')
    if len(objects) == 3:
        uid, timestamp, http = objects[0], int(float(objects[1]) * 1000), objects[2] 
        if int(uid) % 256 == N and http.startswith('http'):
            emit(uid, timestamp, http)

def main():
    connection = happybase.Connection(HOST)
    global table
    table = connection.table(TABLE_NAME)
    for line in sys.stdin:
        try:
            do_map(line.strip())
        except ValueError:
            continue
    connection.close()

if __name__ == '__main__':
    main()

#Всё четко. В целом виден почерк не-python разработчика (академично, что ли). Не хватило описания BASH'овой части, но там в целом всё ясно понятно, особенно когда пару раз сделаешь.

 
#1. Корректен ли выбранный подход с логической точки зрения? - да
#2. Насколько эффективен код и алгоритм решения задачи? - 
#3. Используются ли возможности языка? -  да
#4. Содержит ли код повторяющиеся куски? - нет
#5. Содержит ли код захардкоженные значения/переменные? - нет, но кажется, что TABLE_NAME = 'alexander.alexandrov' HOST = 'bd-node2.newprolab.com' можно было ввести как-то иначе...
#6. Содержит ли код многочисленные условия if/else и циклы (более 3 для условий и более 2 для циклов)? - нет
#7. Содержит ли код длинные функции, состоящие из нескольких веток? - нет
#8. Содержит ли код проверки на null-значения и обработку ошибок (если по условию задачи в этом есть необходимость)? - нет, но здесь это не обязательно
#9. Содержит ли код комментарии? - нет, немного не хватило. есть ощущение, что код скопирован =)
#10. Содержит ли скрипт закомментированный (неиспользуемый) код? - нет и слава богу!
#11. Содержит ли скрипт долгоисполняемые ячейки или циклы? - нет, не актуально
#12. Содержит ли ноутбук заголовки, подзаголовки разных уровней? - нет, не актуально
#13. Понятно ли именование переменных? - да
#14. Соблюдается ли требования к длине строки согласно PEP8 (79 символов для кода, 72 для комментариев и докстрингов)? - ноу комментс
#15. Соблюдаются ли требования к импорту модулей согласно PEP8? - ноу комментс
#16. Соблюдаются ли требования к пробелам согласно PEP8? - ноу комментс
#17. Ограничено ли число строк при выводе датафреймов или серий?- ноу комментс
