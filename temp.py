from __future__ import print_function
from time import sleep
from tqdm import tqdm
from multiprocessing import Pool, freeze_support, RLock


L = list(range(9))


def progresser(n):
    interval = 0.001 / (n + 2)
    total = 5000
    for _ in tqdm(range(total), position=n):
        sleep(interval)
    return n


if __name__ == '__main__':
    print('start')
    p = Pool(len(L))
    temp = set()
    for i in p.imap_unordered(progresser, L):
        temp.add(i)
    print("\n" * (len(L) - 2))
    print(temp)
