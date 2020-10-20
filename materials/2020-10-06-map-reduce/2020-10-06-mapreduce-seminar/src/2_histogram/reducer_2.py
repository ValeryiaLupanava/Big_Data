#!/usr/bin/python3

import sys


def emit(prev_key, ones):
    res = '*' * sum(ones)
    print('{:10}\t{}'.format(prev_key, res))


def reducer():
    prev_key = None
    marks = []
   
    k, v = None, None
    for line in sys.stdin:
        split_line = line.strip().split('\t')
        if len(split_line) != 2:
            continue
        k, v = split_line
        v = float(v)
        if k != prev_key and prev_key is not None:
            emit(prev_key, marks)
            marks = []
        prev_key = k
        marks.append(1)

    if prev_key is not None:
        emit(prev_key, marks)

if __name__ == '__main__':
    reducer()
