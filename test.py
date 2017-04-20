#!/usr/bin/env python3

import unittest
from struct import unpack
from sys import getsizeof
import random

num = 2554
num_byte = num.to_bytes(2, 'little')
print(num_byte)
print(len(num_byte))
print(getsizeof(num_byte))
print(getsizeof(num))
print(getsizeof(4))
# num_from_byte_to_int = unpack('i', num_byte)
# self.assertEqual(num, num_from_byte_to_int, "Not equal")

def get_int_and_byte():
    num = random.randint(0,10000000)
    num_byte = num.to_bytes(4, 'little')
    with open('int_as_byte', 'wb') as f:
        f.write(num_byte)
    with open('int.txt', 'w') as f:
        print(type(f))
        f.write(str(num))

    with open('int_and_byte.txt', 'w') as f:
        line = "{}\t{}".format(num, num_byte)
        f.write(line)

    with open('int_and_byte.txt') as f:
        print("read")
        print(f.seek(0, 2))
        print(f.readline())

        print(f.seek(0, 0))
        print(f.readline())
        print("done")

    print('num: {}, num_byte: {}'.format(num, num_byte))
    return num, num_byte

get_int_and_byte()