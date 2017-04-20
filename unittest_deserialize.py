#!/usr/bin/env python3

import unittest
from struct import unpack
from UnityMeshByteHandler import *
import random
random.seed()

def generate_int_and_byte():
    num = random.randint(0,10000000)
    num_byte = num.to_bytes(4, 'little')
    with open('int_as_byte', 'wb') as f:
        f.write(num_byte)
    with open('int.txt', 'w') as f:
        f.write(str(num))

    with open('int_and_byte.txt', 'w') as f:
        line = "{}\t{}".format(num, num_byte)
        f.write(line)
    print('num: {}, num_byte: {}'.format(num, num_byte))
    return num, num_byte

class ByteTest(unittest.TestCase):

    def get_int_and_byte(self):
        num = random.random()
        num_byte = num.to_bytes(4, 'little')
        print('num: {}, num_byte: {}'.format(num, num_byte))
        return num, num_byte

    def testByteConversion(self):
        num = 4890
        # bytes([n]) constructs a bytes object from an iterable of byte-like int (that is to say in range(0, 256))
        num_byte = num.to_bytes(4, 'little')
        num_from_byte_to_int,  = unpack('i', num_byte)
        self.assertEqual(num, num_from_byte_to_int, "Not equal")

    def test_read_int32(self):
        num = None
        num_byte = None
        with open('int.txt') as f:
            num = int(f.readline())
        with open('int_as_byte', 'rb') as f:
            num_byte = read_int32(f)

        self.assertEqual(num, num_byte, "Not equal")
