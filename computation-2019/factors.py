import collections

def base_210_table():
    pass

def base_prime_list():
    return [2, 3, 5, 7][:]

def factor_1_to_n_fancy(n):
    b210 = base_210_table()
    results = [None]*(1+n)

    primes = base_prime_list()


    return results

def factor_1_to_n_brute(n):
    results = [None]*(1+n)

    primes = base_prime_list()

    results[1] = {}
    for m in range(2, n+1):
        factors = collections.defaultdict(lambda: 0)
        mm = m
        for p in primes:
            if p > mm:
                break
            while mm % p == 0:
                mm //= p
                factors[p] += 1
            if mm == 1:
                break
        if len(factors) == 0:
            factors[m] += 1
            if m > primes[-1]:
                primes.append(m)
        results[m] = dict(factors)

    return results

def factor_1_to_n_recurse(n):
    results = [None]*(1+n)

    primes = [2]
    cutoff = 0
    pco2 = primes[cutoff]**2

    results[1] = collections.defaultdict(lambda: 0)
    for m in range(2, n+1):
        if m == pco2:
            p = primes[cutoff]
            factors = results[1].copy()
            factors[p] += 2
            cutoff += 1
            pco2 = primes[cutoff]**2
        else:
            for p in primes[:cutoff]:
                if m % p == 0:
                    factors = results[m//p].copy()
                    factors[p] += 1
                    break
            else:
                factors = results[1].copy()
                factors[m] += 1
                if m > primes[-1]:
                    primes.append(m)
        results[m] = factors

    return results

def count_prime_powers(factor_list):
    return len([1 for facs in factor_list if len(facs) == 1])

def count_primes(factor_list):
    return len([1 for facs in factor_list if len(facs) == 1 and list(facs.values())[0] == 1])

if __name__ == '__main__':
    maxn = int(1e7)
    facdict = factor_1_to_n_recurse(n=maxn)

    # compute a "factor fingerprint"
    ffp = lambda fd: tuple(sorted(fd.values(), reverse=True))

    if False:
        xx = set([ffp(facdict[i]) for i in range(2, 100)])
        for x in sorted(xx):
            print(x, [i for i in range(2, 100) if ffp(facdict[i]) == x])

    faccount = lambda n: sum([x[1] for x in facdict[n].items()])

    if True:
        match = [3]*7
        match = [2,2,2,None,2,2,2]
        tail = []
        for i in range(1, maxn):
            tail.append(faccount(i))
            if len(tail) < len(match):
                continue
            if len(tail) > len(match):
                tail = tail[-len(match):]
            for t, m in zip(tail, match):
                if m != None and t == m:
                    continue
                break
            else:
                print('Match {}:  {} & preceding'.format(match, i))

    if False:
        triggers = [False, False, False, False, False]

        summary = collections.defaultdict(lambda: 0)
        for i in range(1, maxn):
            summary[faccount(i)] += 1

            for j in range(1, 5):
                if summary[j] > summary[j-1] and not triggers[j]:
                    triggers[j] = True
                    print('*** n=', i, '***')
                    for k in range(14):
                        if summary[k] == 0:
                            break
                        print(summary[k])

    if False:

        print(facdict[97])
        print(facdict[10])
        print(facdict[34])
        #print(facdict[1000])
        print(facdict[729])
        print(facdict[63])

    if False:
        print('****')
        for i in range(10):
            a, b = max(i*100000, 2), ((i+1)*100000)
            print(a, b-1, count_prime_powers(facdict[a:b]), count_primes(facdict[a:b]))
