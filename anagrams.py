#! /usr/bin/python
import json
import argparse
import itertools
import multiprocessing
import time

from tqdm import tqdm


def load_json(path):
    with open(path) as f:
        return json.load(f)


def load_words():
    return load_json('words/words.json.min')


def load_search_dict():
    return load_json('anagrams/search_dict.json')


def get_all_permutations(word):
    return list(itertools.permutations(word))


def handle_arguments():
    parser = argparse.ArgumentParser(description='Anagram finder script.')
    parser.add_argument('limit', metavar='N', type=int, help='inclusive character search limit')
    return  parser.parse_args()


def find_anagrams_for_word(pos):
    words = target_words[pos]
    results = set()

    for word in tqdm(words, desc='Thread {}'.format(pos), position=pos):
        w = word.lower()
        permutations = [''.join(p) for p in list(itertools.permutations(w))]
        temp = set([word])

        length = str(len(w))
        for p in permutations:
            try:
                search_list = [w.lower() for w in search_dict[p[0]][length]]
            except KeyError:
                continue
            if p in search_list:
                temp.add(p)

        if len(temp) > 1:
            results.add(frozenset(temp))

    return results


def chunk_it(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


if __name__ == '__main__':
    args = handle_arguments()
    words = load_words()
    search_dict = load_search_dict()
    limit = args.limit
    pool_count = multiprocessing.cpu_count()
    STARTED = time.time()


    print('>> searching anagrams with character limit {} on {} threads..'.format(limit, pool_count))

    target_words = [w for w in words if len(w) <= limit]

    target_words = chunk_it(target_words, pool_count)

    results = set()

    pool = multiprocessing.Pool(pool_count)
    for res in pool.imap(find_anagrams_for_word, list(range(pool_count))):
        results = results.union(res)
        
    results = list(results)
    for i in range(len(results)):
        results[i] = ' - '.join(list(results[i]))

    results.sort()
    print("\n" * (pool_count - 2))
    print('>> {} anagrams were found'.format(len(results)))

    path = 'anagrams/anagrams-{}.json'.format(limit)
    with open(path, 'w') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print('>> results written to "{}"'.format(path))

    FINISHED = time.time()
    print('>> finished in {0:.2f} seconds'.format(FINISHED - STARTED))
