import re
import collections

counter = collections.Counter()

x = re.compile('[0-9, ]{13}-')

cuts = ['{:20,}'.format(2**i) for i in range(46)]
cuts.reverse()

with open('series3-unified.txt', 'r') as f1:
    for index, line in enumerate(f1):
        M, power = line.rstrip().split('-')
        for ct in cuts:
            if M >= ct:
                key = (int(power.strip()), ct)
                counter.update([key])
                break

with open('series3-summary.txt', 'w') as f2:
    for line, count in sorted(counter.items()):
        f2.write('{:14,} {} {}\n'.format(count, line[0], line[1]))
