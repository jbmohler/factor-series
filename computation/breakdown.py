import collections
import sympy.ntheory as ntheory

def count_factors(n):
    ff = ntheory.factorint(n)
    return sum([mult for _, mult in ff.items()])

x = [count_factors(nn) for nn in range(1400000, 1500000)]

ccc = collections.Counter(x)

for factors, count in sorted(ccc.items()):
    print(factors, count)
