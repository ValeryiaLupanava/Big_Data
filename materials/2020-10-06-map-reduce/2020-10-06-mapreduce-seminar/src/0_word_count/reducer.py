#!/usr/bin/python3

import sys

prev_key = None
sum = 0

for line in sys.stdin:
    key, value = line.split("\t") 
    if key != prev_key and prev_key is not None:
        print(prev_key, sum)
        sum = 0
    sum += 1
    prev_key = key

if prev_key is not None:
    print(prev_key, sum)
