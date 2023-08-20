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
        return "{0._base:20,}-{0._n:2}\n".format(self)

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


class SeqFilter:
    def __init__(self, m3, candidates):
        self.mega = m3
        self.candidates = candidates


@functools.cache
def mask(mega3):
    candidates = []
    for base in range(0, mega3, 8):
        seqordering = []
        for i in range(1, 8):
            g = sympy.gcd(base + i, mega3)
            gfaccount = count_factors(g)
            if gfaccount >= 3:
                break

            seqordering.append((i, g, gfaccount))
        else:
            seqordering.sort(key=lambda sot: sot[2], reverse=True)
            candidates.append((base, seqordering))
    return SeqFilter(mega3, candidates)


def mask_from(mega3, sfilter):
    fac = mega3 // sfilter.mega
    candidates = []
    for ifac in range(fac):
        # only need to look at candidates of the lower order filter
        for offset, _ in sfilter.candidates:
            base = ifac * sfilter.mega + offset
            assert base < mega3
            seqordering = []
            for i in range(1, 8):
                g = sympy.gcd(base + i, mega3)
                gfaccount = count_factors(g)
                if gfaccount >= 3:
                    break

                seqordering.append((i, g, gfaccount))
            else:
                seqordering.sort(key=lambda sot: sot[2], reverse=True)
                candidates.append((base, seqordering))
    return SeqFilter(mega3, candidates)


BASE_BUILD_FACTORS = [8, 3, 5, 3, 7, 3, 11, 5, 13]

# candidates is a list of 2-tuples with and offset and optimized ordering for
# checking the next 7 integers for being 3-almost-prime
# (offset, [(seq-offset, divisor, divisor-factor-count), ....])
# Here the list of seq-offsets must be of length 7 and should be ordered
# descending by divisor-factor-count

sfilter = None
for fac in BASE_BUILD_FACTORS:
    if not sfilter:
        sfilter = mask(fac)
    else:
        sfilter = mask_from(sfilter.mega * fac, sfilter)

    print(
        sfilter.mega,
        sfilter.mega // 8,
        len(sfilter.candidates),
        round((len(sfilter.candidates) / (sfilter.mega // 8)) * 100, 1),
    )
    # for cand in sfilter.candidates[:2]:
    #    print(cand)


def test_m_mega(m, sfilter):
    n = 3
    candidates = sfilter.candidates

    def countfail_by_plan(base, plan):
        u, divisor, divfac = plan
        test = (base + u) // divisor
        if divfac + 1 == n:
            return not ntheory.isprime(test)
        else:
            return count_factors(test) + divfac != n

    layerbase = m * sfilter.mega
    for c, testplan in candidates:
        base = layerbase + c

        if any((countfail_by_plan(base, plan) for plan in testplan)):
            continue

        nr = NeighborRange(base, n)
        yield nr
        while True:
            esc = escalated(nr)
            if esc == None:
                break
            yield esc
            nr = esc


def test_m_mega_list(m, sfilter):
    return list(test_m_mega(m, sfilter))


GLOBAL_FILTER = sfilter


def my_mega_list(m):
    global GLOBAL_FILTER
    return list(test_m_mega(m, GLOBAL_FILTER))


import workstream

if __name__ == "__main__":
    MAX = 10 * 1_000_000

    def chunks():
        func = my_mega_list

        for o1 in range(0, MAX):
            yield (func, (o1,), {})

    with open("series3-u2.txt", "w") as f:
        layer_count = 0
        write_count = 0
        for results in workstream.work_stream(chunks()):
            layer_count += 1
            write_count += len(results)
            data = "".join([repr(nb) for nb in results])
            f.write(data)

            if layer_count % 5000 == 0:
                print(f"Wrote {write_count} in layer {layer_count}")
            f.flush()
