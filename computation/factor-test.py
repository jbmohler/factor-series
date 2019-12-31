#!/usr/bin/env python
import sys
import time
import sympy.ntheory as ntheory

exp = int(sys.argv[1])
size = int(sys.argv[2])

s1 = time.time()

base = 2**exp
for i in range(size):
    ntheory.factorint(base+i+1)

s2 = time.time()

print('2**{} -- size {} -- {:7.3f}'.format(exp, size, s2-s1))
