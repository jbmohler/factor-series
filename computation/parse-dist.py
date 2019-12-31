import re
import math
import collections

class FormattableNone(object):
    def __format__(self, format_spec):
        return '-'*int(format_spec[0])

FNone = FormattableNone()

def parse_dist(which):
    table = {}

    fname = 'apdist2-out.txt' if which == 'all' else 'apdist2-out-odd.txt'

    with open(fname, 'r') as f:
        lines = f.readlines()

        for line in lines:
            l = line.strip()
            if '-' in l:
                n1, n2 = l.split(' - ')
                n1 = int(n1.strip().replace(',', ''))
                n1 = int(math.log2(n1))

                current = n1
                table[current] = {}

            elif '*' in l:
                continue
            else:
                n1, n2 = re.split(' *', l.strip())

                table[current][int(n1)] = int(n2)

    for index in sorted(table.keys()):
        col = table[index]
        avgd = 2**index
        if which != 'all':
            avgd //= 2
        ss = sum([key * quan for key, quan in col.items()]) / avgd

        lsdd = sum([quan for key, quan in col.items() if key <= ss])
        if lsdd == 0:
            lsd = FNone
        else:
            lsd = sum([quan*(key-ss)**2 for key, quan in col.items() if key <= ss]) / lsdd
            lsd = math.sqrt(lsd)
        rsdd = sum([quan for key, quan in col.items() if key >= ss])
        if rsdd == 0:
            rsd = FNone
        else:
            rsd = sum([quan*(key-ss)**2 for key, quan in col.items() if key >= ss]) / rsdd
            rsd = math.sqrt(rsd)

        #quans = '-'.join(['{:,}'.format(quan) for key, quan in sorted(col.items())])

        def fx(v):
            if v == None:
                return '{:>10} ( -- )'.format('-')
            else:
                base = 2**index
                if which != 'all':
                    base //= 2
                perc = v / base * 100
                return '{:10,} ({:3.0f}%)'.format(v, perc)
        quans = '  '.join([fx(col.get(x, None)) for x in range(1, 5)])

        print('{:4}  {:5.3f}  {:5.3f}  {:5.3f}  {}'.format(index, lsd, ss, rsd, quans))

def count_by_pow2():
    def xx():
        with open('series3-unified.txt', 'r') as ff:
            for row in ff:
                num, series = row.split('-')
                blah = int(series.strip())
                pow2 = int(math.log2(float(num.strip().replace(',', ''))))

                yield (blah, pow2)

    cc = collections.Counter(xx())

    for thing in sorted(cc.items()):
        print(thing)

#parse_dist('all')
#parse_dist('odd')

count_by_pow2()
