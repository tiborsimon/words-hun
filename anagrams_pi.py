#! /usr/bin/python
import json
import argparse
import itertools
import time
import signal
import sys
import os


from tqdm import tqdm


def load_json(path):
    with open(path) as f:
        return json.load(f)


def load_words():
    return load_json('words/words.json.min')


def load_search_dict():
    return load_json('anagrams/search_dict.json')

def load_progress(limit):
    return load_json('anagrams/progress-{}.json'.format(limit))


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


def interrupt_handler(*args):
    print(' interrupted by user, saving progress..')
    path = 'anagrams/progress-{}.json'.format(limit)
    progress['anagrams'] = [list(a) for a in progress['anagrams']]
    with open(path, 'w') as f:
        json.dump(progress, f, indent=4, ensure_ascii=False)
    print('>> progress saved to {}'.format(path))
    sys.exit(0)


if __name__ == '__main__':
    args = handle_arguments()
    words = load_words()
    search_dict = load_search_dict()
    limit = args.limit
    STARTED = time.time()

    signal.signal(signal.SIGINT, interrupt_handler)
    signal.signal(signal.SIGTERM, interrupt_handler)


    print('>> searching anagrams with character limit {}..'.format(limit))

    target_words = [w for w in words if len(w) <= limit]

    try:
        progress = load_progress(limit)
        progress['anagrams'] = set([frozenset(a) for a in progress['anagrams']])
        progress_loaded = True
        print('>> previous progress loaded')
    except:
        progress = {
            'finished_words': [],
            'anagrams': set()
        }
        progress_loaded = False


    for word in tqdm(target_words):
        if word in progress['finished_words']:
            continue

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
            progress['anagrams'].add(frozenset(temp))

        progress['finished_words'].append(word)
    else:
        results = list(progress['anagrams'])
        for i in range(len(results)):
            results[i] = ' - '.join(list(results[i]))

        results.sort()
        print('>> {} anagrams were found'.format(len(results)))

        path = 'anagrams/anagrams-{}.json'.format(limit)
        with open(path, 'w') as f:
            json.dump(results, f, indent=4, ensure_ascii=False)

        print('>> results written to "{}"'.format(path))

        if progress_loaded:
            os.remove('anagrams/progress-{}.json'.format(limit))
            print('>> progress file removed')

        FINISHED = time.time()
        print('>> finished in {0:.2f} seconds'.format(FINISHED - STARTED))
