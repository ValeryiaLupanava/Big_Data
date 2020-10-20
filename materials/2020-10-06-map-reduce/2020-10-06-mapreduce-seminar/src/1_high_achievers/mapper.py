#!/usr/bin/python3

import sys

def emit(key, value):
    sys.stdout.write('{}\t{}\n'.format(key, value))

def map(line):
    objects = line.split('\t')
    if len(objects) == 2:
        name, score = objects
        emit(name, score)

def main():
    for line in sys.stdin:
        map(line.strip())

if __name__ == '__main__':
    main()
