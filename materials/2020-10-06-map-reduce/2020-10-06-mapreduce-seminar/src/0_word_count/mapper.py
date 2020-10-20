#!/usr/bin/python3

import sys

def emit(key, value):
    sys.stdout.write('{}\t{}\n'.format(key, value))

def map(line):
    for token in line.lower().split(' '):
        emit(token, 1)

def main():
    for line in sys.stdin:
        map(line)

if __name__ == '__main__':
    main()
