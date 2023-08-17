import functools
import sympy
import sympy.ntheory as ntheory


def count_factors(n):
    ff = ntheory.factorint(n)
    return sum([mult for _, mult in ff.items()])


class NeighborRange:
    def __init__(self, base, n):
        self._base = base
        self._n = n

    def __repr__(self):
        return "{0._base:20,}-{0._n:2}".format(self)

    def __str__(self):
        return "str-NeighborRange({0._base}, {0._n})".format(self)


def escalated(nr):
    n = nr._n + 1
    base = nr._base * 2
    untested = list([2 * i + 1 for i in range(2 ** (n - 1))])
    test2 = any((count_factors(base + u) != n for u in untested))
    if not test2:
        return NeighborRange(base, n)
    return None


MEGA3 = 8 * 27 * 25 * 7 * 11 * 13
print(MEGA3)


@functools.cache
def mask(mega3):
    candidates = []
    for base in range(0, mega3, 8):
        for i in range(1, 8):
            g = sympy.gcd(base + i, mega3)
            if count_factors(g) >= 3:
                break
        else:
            candidates.append(base)
    return candidates


mega_list = [
    8,
    8 * 27,
    8 * 27 * 25,
    8 * 27 * 25 * 7,
    8 * 27 * 25 * 7 * 11,
    8 * 27 * 25 * 7 * 11 * 13,
]


for mega3 in mega_list:
    testbases = mask(mega3)
    print(len(testbases), mega3 // 8, round((len(testbases) / (mega3 // 8)) * 100, 1))


def test_m_mega(m):
    n = 3
    untested = list(range(1, 8))
    candidates = mask(MEGA3)

    for c in candidates:
        base = m * MEGA3 + c

        if any((count_factors(base + u) != n for u in untested)):
            continue

        nr = NeighborRange(base, n)
        yield nr
        while True:
            esc = escalated(nr)
            if esc == None:
                break
            yield esc
            nr = esc


def test_m_mega_list(m):
    return list(test_m_mega(m))


import workstream

if __name__ == "__main__":
    MAX = 20

    def chunks():
        func = test_m_mega_list

        for o1 in range(0, MAX):
            # print(f'Layer {o1} of {MAX}')
            yield (func, (o1,), {})

    with open("series3-u2.txt", "w") as f:
        layer_count = 0
        write_count = 0
        for results in workstream.work_stream(chunks()):
            layer_count += 1
            for nb in results:
                write_count += 1
                f.write(repr(nb) + "\n")

                if write_count % 1000 == 0:
                    print(f"Wrote {write_count} in layer {layer_count}")
            f.flush()
