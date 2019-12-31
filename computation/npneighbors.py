#!/usr/bin/env python
import os
import sys
import time
import math
import datetime
import concurrent.futures as futures
import sympy.ntheory as ntheory

def get_mask210():
    """
    >>> m210 = get_mask210()
    >>> len(m210) < 210*.25
    True
    """
    mask210 = list(range(210))
    for p in [2, 3, 5, 7]:
        mask210 = [m for m in mask210 if m % p != 0]
    return mask210

def get_mask630():
    """
    >>> m630 = get_mask630()
    >>> len(m630) < 195
    True
    """
    m630 = []
    m210 = get_mask210()
    for p in range(630):
        if p % 3 == 1:
            continue
        if p % 3 == 0:
            r0 = 4*p//3+1
            if (r0 % 210) in m210:
                m630.append(p)
        if p % 3 == 2:
            r2 = 4*(p-2)//3+3
            if (r2 % 210) in m210:
                m630.append(p)
    return m630

#def is_prime(xx):
#    """
#    >>> assert is_prime(2)
#    >>> assert not is_prime(8)
#    >>> assert is_prime(31)
#    >>> assert not is_prime(92)
#    >>> assert not is_prime(35)
#    >>> assert not is_prime(121)
#    """
#    assert xx > 0
#    if xx in [2, 3, 5, 7]:
#        return True
#    if xx in [4, 6, 8, 9]:
#        return False
#    top = int(math.sqrt(xx) + 1)
#    for yy in range(2, top):
#        if xx % yy == 0:
#            return False
#    return True
#
#def count_factors(xx):
#    """
#    >>> assert count_factors(30) == 3
#    >>> assert count_factors(19) == 1
#    >>> assert count_factors(8) == 3
#    >>> assert count_factors(39) == 2
#    >>> assert count_factors(97) == 1
#    >>> assert count_factors(25) == 2
#    """
#    assert xx > 0
#    if xx == 1:
#        return 0
#    if xx in [2, 3, 5, 7]:
#        return 1
#    if xx in [4, 6, 9]:
#        return 2
#    if xx == 8:
#        return 3
#    top = int(math.sqrt(xx) + 1)
#    temp = xx
#    count = 0
#    for yy in range(2, top):
#        while temp % yy == 0:
#            count += 1
#            temp /= yy
#        if temp == 1:
#            break
#    if temp > top:
#        count += 1
#    return count
#
def is_prime(n):
    return ntheory.isprime(n)

def count_factors(n):
    ff = ntheory.factorint(n)
    return sum([mult for _, mult in ff.items()])

class NeighborRange:
    def __init__(self, base, n):
        self._base = base
        self._n = n

    def __repr__(self):
        return '{0._base:20,}-{0._n:2}'.format(self)

    def __str__(self):
        return 'str-NeighborRange({0._base}, {0._n})'.format(self)

def escalated(nr):
    n = nr._n + 1
    base = nr._base * 2
    untested = list([2*i + 1 for i in range(2**(n-1))])
    test2 = any((count_factors(base + u) != n for u in untested))
    if not test2:
        return NeighborRange(base, n)
    return None

def test_range_star630(n, base1, base2):
    assert n >= 2
    mult = 2 ** n
    md4 = 2 ** (n-2)
    untested = [z for z in range(1, mult) if z % md4 != 0]

    m630 = get_mask630()

    for i in range(base1, base2):
        for j in m630:
            M = i*630 + j
            base = M*mult

            xmid = 2*M + 1
            if M % 3 == 0:
                xoff = 4*M // 3 + 1
                punk = base + md4
            if M % 3 == 2:
                xoff = 4*(M - 2)//3 + 3
                punk = base + 3*md4
            test1 = is_prime(xmid) and \
                    is_prime(xoff) and \
                    count_factors(punk) == n
            if test1 and len(untested) > 0:
                test2 = any((count_factors(base + u) != n for u in untested))
                test1 = not test2
            if test1:
                nr = NeighborRange(base, n)
                yield nr
                while True:
                    esc = escalated(nr)
                    if esc == None:
                        break
                    yield esc
                    nr = esc

def test_range_star630_timed(n, base1, base2):
    t1 = time.time()
    results = list(test_range_star630(n, base1, base2))
    t2 = time.time()
    print('  Time {:.2f} (PID {})'.format(t2-t1, os.getpid()))
    return results

if __name__ == '__main__':
    #test_range_star630(2, 0, 1)
    #test_range_star630(3, 0, 1000)

    with open('series3-unified.txt', 'w') as f:
        pass
    func = test_range_star630_timed
    for o1 in range(0, 3000):
        print('Layer {} of {}'.format(o1, 200))
        with futures.ProcessPoolExecutor(max_workers=6) as tp:
            waiting = [tp.submit(func, 2, xd*1000, (xd+1)*1000) for xd in range(o1*16, (o1+1)*16)]

            with open('series3-unified.txt', 'a') as f:
                for fut in waiting:
                    for nb in fut.result():
                        f.write(repr(nb)+'\n')
