#!/usr/bin/env python
import sys
import datetime
import sympy.ntheory as ntheory

def get_mask210():
    mask210 = list(range(210))
    for p in [2, 3, 5, 7]:
        mask210 = [m for m in mask210 if m % p != 0]
    return mask210

is_threefac = lambda n: sum([mult for fac, mult in ntheory.factorint(n).items()]) == 3
is_fourfac = lambda n: sum([mult for fac, mult in ntheory.factorint(n).items()]) == 4
is_fivefac = lambda n: sum([mult for fac, mult in ntheory.factorint(n).items()]) == 5

def test_fourfac():
    print(is_fourfac(32))
    print(is_fourfac(97*2*3*11))

def ptableline(a):
    print('\t'.join([str(x) for x in a]))

def gen_210_advanced():
    mask210 = get_mask210()

    count = 0
    for N in range(210*6):
        use = False
        if (N + 2) % 3 == 0:
            a = [N] + ['-']*6
        if (N + 1) % 3 == 0:
            x1 = 2*N+1
            assert (4*N+1) % 3 == 0
            x2 = (4*N+1)//3
            a = [N, x1, x1%210 in mask210, '-', '-', x2, x2%210 in mask210]
            use = x1%210 in mask210 and x2%210 in mask210
        if N % 3 == 0:
            x1 = 2*N+1
            assert 4*N % 3 == 0
            x2 = 4*N//3+1
            a = [N, x1, x1%210 in mask210, x2, x2%210 in mask210, '-', '-']
            use = x1%210 in mask210 and x2%210 in mask210
        if use:
            a += ['!!']
            count += 1
        ptableline(a)
    print(count)

def pretty_facs(n):
    factors = ntheory.factorint(n)
    fstr = []
    for prime, power in sorted(factors.items()):
        if power == 1:
            s = str(prime)
        else:
            s = '{}^{}'.format(prime, power)
        fstr.append(s)
    return ' * '.join(fstr)

def search_slow_loop3():
    mask210 = set(get_mask210())

    for N in range(1000):
        base = N * 8
        if not is_threefac(base+4):
            continue
        odds = [base + odd for odd in [1, 3, 5, 7]]
        evens = [base + even for even in [2, 6]]
        exceptions = [x for x in odds+evens if not is_threefac(x)]
        if len(exceptions) < 2:
            print('**** {} ****'.format(base))
            for x in range(1, 2**3):
                print('{} = {} {}'.format(base+x, pretty_facs(base+x), '>>> exc <<<' if not is_threefac(base+x) else ''))

def search_slow_loop4(basemill):
    mask210 = set(get_mask210())

    #target = 26117740881//16
    #for N in range(target-30, target+30):
    for N in range(10000000*basemill, 10000000*(basemill+1)):
        if (N + 2) % 3 == 0:
            continue
        x1 = 2*N+1
        if not x1%210 in mask210:
            continue
        if (N + 1) % 3 == 0:
            assert (4*N+1) % 3 == 0
            x2 = (4*N+1)//3
            if not x2%210 in mask210:
                continue
        if N % 3 == 0:
            assert 4*N % 3 == 0
            x2 = 4*N//3+1
            if not x2%210 in mask210:
                continue

        base = N * 16
        if not ntheory.isprime(x1):
            continue
        if not ntheory.isprime(x2):
            continue
        #if not is_fourfac(base+8):
        #    continue
        if N % 3 == 0:
            if not is_fourfac(base+4):
                continue
        if (N + 1) % 3 == 0:
            if not is_fourfac(base+12):
                continue
        odds = [base + odd for odd in [1, 3, 5, 7, 9, 11, 13, 15]]
        evens = [base + even for even in [2, 6, 10, 14]]
        exceptions = 0
        for x in odds+evens:
            if not is_fourfac(x):
                exceptions += 1
                if exceptions > 2:
                    break
        if exceptions < 3:
            print('**** {} ****'.format(base))
            for x in range(1, 2**4):
                print('{} = {} {}'.format(base+x, pretty_facs(base+x), '>>> exc <<<' if not is_fourfac(base+x) else ''))

def search_slow_loop5(basemill):
    mask210 = set(get_mask210())

    #target = 26117740881//16
    #for N in range(target-30, target+30):
    for N in range(10000000*basemill, 10000000*(basemill+1)):
        #if (N + 2) % 3 == 0:
        #    continue
        x1 = 2*N+1
        if not x1%210 in mask210:
            continue
        if (N + 1) % 3 == 0:
            assert (4*N+1) % 3 == 0
            x2 = (4*N+1)//3
        #    if not x2%210 in mask210:
        #        continue
        if N % 3 == 0:
            assert 4*N % 3 == 0
            x2 = 4*N//3+1
        #    if not x2%210 in mask210:
        #        continue

        base = N * 32
        if not ntheory.isprime(x1):
            continue
        if not ntheory.isprime(x2):
            continue
        if N % 3 == 0:
            if not is_fivefac(base+8):
                continue
        if (N + 1) % 3 == 0:
            if not is_fivefac(base+24):
                continue
        odds = [base + odd for odd in range(1, 32, 2)]
        evens = [base + even for even in range(2, 32, 2) if even not in (8, 16, 24)]
        exceptions = 0
        for x in odds+evens:
            if not is_fivefac(x):
                exceptions += 1
                if exceptions > 2:
                    break
        if exceptions < 3:
            print('**** {} ****'.format(base))
            for x in range(1, 2**5):
                print('{} = {} {}'.format(base+x, pretty_facs(base+x), '>>> exc <<<' if not is_fivefac(base+x) else ''))


if __name__ == '__main__':
    a1, a2 = sys.argv[1:]
    assert a1 in '345'
    assert 0 <= int(a2) < 100000
    if a1 == '3':
        search_slow_loop3()
    elif a1 == '4':
        search_slow_loop4(int(a2))
    elif a1 == '5':
        search_slow_loop5(int(a2))
    #else:
        #for x in range(1000):
        #    sys.stderr.write('searching {} -- {}\n'.format(x*1e6, datetime.datetime.now()))
        #    search_slow_loop4(x)
    #gen_210_advanced()

"""
for g210 in range(10000000, 20000000):
    for m210 in mask210:
        p = g210*210+m210
        if is_prime(p):
            hook12 = p*12
            hook8 = hook12 - 4 if hook12 % 16 == 12 else hook12 + 4
            if (hook8 // 8).is_prime():
                # investigate more
                odds = [hook8 + odd for odd in range(-7, 9, 2)]
                evens = [hook8 + even for even in range(-6, 8, 2) if even != 0]
                exceptions = [x for x in odds+evens if not is_fourfac(x)]
                if len(exceptions) < 3:
                    print('**** {} *** {}'.format(g210, p))
                    for x in range(-7, 8):
                        print('{} = {} {}'.format(hook8+x, factor(hook8+x), '>>> exc <<<' if not is_fourfac(hook8+x) else ''))


**** 10364182 *** 2176478407
26117740881 = 3^2 * 127 * 22850167 
26117740882 = 2 * 7109 * 1836949 >>> exc <<<
26117740883 = 13 * 17 * 4051 * 29173 
26117740884 = 2^2 * 3 * 2176478407 
26117740885 = 5 * 79 * 439 * 150617 
26117740886 = 2 * 167 * 2909 * 26881 
26117740887 = 3 * 7 * 18793 * 66179 
26117740888 = 2^3 * 3264717611 
26117740889 = 43 * 827 * 857^2 
26117740890 = 2 * 3^2 * 5 * 290197121 >>> exc <<<
26117740891 = 11 * 83 * 181 * 158047 
26117740892 = 2^2 * 53 * 123196891 
26117740893 = 3 * 37 * 179 * 1314497 
26117740894 = 2 * 7 * 101 * 18470821 
26117740895 = 5 * 29 * 3931 * 45821 


for mult in range(1000):
    base = mult * 16
    if not is_fourfac(base+8):
        continue
    if not is_fourfac(base+4):
        continue
    if not is_fourfac(base+12):
        continue
    odds = [base + odd for odd in [1, 3, 5, 7, 9, 11, 13, 15]]
    evens = [base + even for even in [2, 6, 10, 14]]
    exceptions = [x for x in odds+evens if not is_fourfac(x)]
    if len(exceptions) < 3:
        print('**** {} ****'.format(base))
        for x in range(1, 16):
            print('{} = {} {}'.format(base+x, factor(base+x), '>>> exc <<<' if not is_fourfac(base+x) else ''))
"""
