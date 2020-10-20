#!/usr/bin/python3

import sys


def emit(key, values):
    avg = sum(values) / len(values)
    if avg >= 4.5:
        print('{}\t{:.2f}'.format(key, avg))

def reducer():
    prev_key = None
    scores = []

    k, v = None, None
    for line in sys.stdin:
        split_line = line.strip().split('\t')
        if len(split_line) != 2:
            continue
        k, v = split_line
        v = float(v)
        if k != prev_key and prev_key is not None:
            emit(k, scores)
            scores = []
        prev_key = k
        scores.append(v)

    if prev_key is not None:
        emit(k, scores)

if __name__ == '__main__':
    reducer()
