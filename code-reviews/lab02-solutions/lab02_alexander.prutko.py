# Решение состоит из двух файлов, находящихся в папке app:
# map_reduce.py - содержит базовый класс Mapper
# mapper_hbase.py - содержит реализацию HBaseMapper для выполнения вставки данных в hbase (должен быть исполняемым)
# Команда запуска задачи:
# hadoop jar ./hadoop-streaming.jar -D mapred.reduce.tasks=0 -files=app -input /labs/lab02data/facetz_2015_02_27/* -output /user/alexander.prutko/lab02/result -mapper "app/mapper_hbase.py"
# 
# Решение может показаться громоздким, но файл map_reduce.py уже несколько раз использовался в разных задачах без изменений
# (в оригинальном map_reuce.py так же есть базовый класс Reducer)
# Наследующий класс как правило получался маленьким, но в этой задаче немного распух :)
# Тут пришлось переопределить метод emit, добавить подключение к hbase и работа с ним

# map_reduce.py
import sys
from abc import ABC, abstractmethod


class Mapper(ABC):
    """
    Абстрактный класс Mapper, реализующий базовую логику
    """
    def map_gen(self, line):
        """
        map_gen генерирует выходные пары ключ/значение из входящей строки
        """
        for key, value in self.parse_line_gen(line):
            yield self.do_map(key, value)

    def emit(self, key, value):
        """
        emit выводит полученные пары ключ/значение
        При необходимости переопределить в наследующем классе
        """
        sys.stdout.write('{}\t{}\n'.format(key, value))

    def __call__(self):
        """
        Вызов маппера
        """
        for line in sys.stdin:
            for key, value in self.map_gen(line):
                if key != None:
                    self.emit(key, value)

    @abstractmethod
    def parse_line_gen(self, line):
        """
        parse_line_gen генерирует входные пары ключ/значение для map_gen из входящей строки
        Необходимо реализовать в наследующем классе
        """
        raise NotImplementedError
    
    @abstractmethod
    def do_map(self, key, value):
        """
        do_map осуществляет отображение пары ключ/значение в новые ключ/значение
        Необходимо реализовать в наследующем классе
        """
        raise NotImplementedError

# mapper_hbase.py
#!/opt/anaconda/envs/bd9/bin/python

import happybase
from map_reduce import Mapper

none_obj = (None, None, None)

class HBaseMapper(Mapper):
    """
    Реализация маппера для вывода результата в hbase
    """
    
    def __init__(self, host, table_name, col_name):
        """
        Инициализация маппера
        host: адрес hbase
        table_name: имя таблицы, в которую будет осуществлен вывод
        col_name: имя column_family, в которую будет осуществлена запись
        """
        table_name = table_name.encode("utf-8")
        self.connection = happybase.Connection(host)
        # Если таблицы не существует, создается новая
        if table_name not in self.connection.tables():
            self.connection.create_table(
                table_name,
                {col_name: dict(max_versions=4096)}
            )
        self.table = self.connection.table(table_name)
        self.col = col_name.encode('utf-8')    

    def parse_line(self, line):
        """
        Парсинг строки. Получение uid, timestamp и url.
        В случае некорректной строки возвращается (none_obj, False)
        """
        user_inf = line.strip().split('\t')
        if len(user_inf) != 3:
            return none_obj, False
        uid, timestamp, url = user_inf
        if not uid.isdigit():
            return none_obj, False
        try:
            ts = str(int(float(timestamp)*1000))
        except ValueError:
            return none_obj, False
        if not url.startswith("http"):
            return none_obj, False
            
        return (int(uid), ts, url), True

    def parse_line_gen(self, line):
        """
        Генерация пары ключ/значение из прочитанной строки
        В случае некорректной строки возвращается (None, None)
        """
        (uid, timestamp, url), ok = self.parse_line(line)
        key = None
        value = None
        if ok:
            key = uid
            value = timestamp + ',' + url

        yield key, value 

    def do_map(self, key, value):
        """
        Идентичное преобразование пары ключ/значение.
        В случае, не удовлетворяющем фильтру, возвращается (None, None)
        """
        k = None
        v = None
        if key is not None and key % 256 == 205:
            k = str(key)
            v = value
        return k, v
    
    def emit(self, key, value):
        """
        Переопределение вывода пары ключ/значение
        Вывод в hbase
        """
        ts, val = value.strip().split(',')
        self.table.put(key.encode('utf-8'), 
            {self.col: val.encode('utf-8')}, timestamp=int(ts))    


def main():
    # Инициализация и вызов маппера. Вывод осуществляется в hbase
    hbase_mapper = HBaseMapper('bd-node2.newprolab.com', 'alexander.prutko', 'data:url')
    hbase_mapper()

if __name__ == '__main__':
    main()
