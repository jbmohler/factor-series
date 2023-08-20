import os
import itertools
import concurrent.futures as futures


def work_stream(gen):
    cpus = os.cpu_count()

    workers = cpus
    if cpus <= 2:
        workers = cpus
    elif cpus <= 8:
        workers = cpus - 1
    else:
        workers = int(cpus * 0.9)

    queue = []
    with futures.ProcessPoolExecutor(max_workers=workers) as tp:
        # pre-stuff the executor with enough of work to have max running
        for func, args, kwargs in itertools.islice(gen, 0, workers * 2):
            queue.append(tp.submit(func, *args, **kwargs))

        while len(queue):
            fut = queue.pop(0)

            # waits
            yield fut.result()

            try:
                (func, args, kwargs) = next(gen)
                queue.append(tp.submit(func, *args, **kwargs))
            except StopIteration:
                pass
