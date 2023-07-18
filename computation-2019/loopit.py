#!/usr/bin/env python
import datetime
import subprocess
import concurrent.futures as futures

def do_series15(i):
    print(datetime.datetime.now(), '----', i)
    x = subprocess.check_output(["python", "series15.py", "4", str(i)])
    return x.decode('ascii')

if __name__ == '__main__':
    chunks = 16
    for xdiv4 in range(15000):
        x = xdiv4 * chunks
        with futures.ThreadPoolExecutor(max_workers=4) as tp:
            futures = [tp.submit(do_series15, x+offset) for offset in range(chunks)]

            with open('series15-threaded.txt', 'a') as f:
                for fut in futures:
                    f.write(fut.result())
