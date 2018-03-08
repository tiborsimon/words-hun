import json
import argparse
import itertools
import subprocess
import time

from tqdm import tqdm
from hashlib import md5


def load_json(path):
    with open(path) as f:
        return json.load(f)


def load_words():
    return load_json('../words/words.json.min')


def get_all_permutations(word):
    return [''.join(p) for p in list(itertools.permutations(word))]


def handle_arguments():
    parser = argparse.ArgumentParser(description='Anagram finder script.')
    parser.add_argument('limit', metavar='N', type=int, help='inclusive character search limit')
    return  parser.parse_args()

def process_word(word):
    res = set([word])
    perms = get_all_permutations(word)
    with open('_p.txt', 'w') as f:
        for p in perms:
            p = p.lower()
            f.write(p)
            f.write('\t')
            f.write(md5(p.encode()).hexdigest())
            f.write('\n')
        proc = subprocess.Popen(['./db_search.sh'], stdout=subprocess.PIPE) 
        (out, err) = proc.communicate()
        print(out)

    return res


if __name__ == '__main__':
    args = handle_arguments()
    words = load_words()

    print('>> searching anagrams with character limit {}..'.format(args.limit))

    target_words = [w for w in words if len(w) <= args.limit]

    results = set()
    for word in (target_words):
        res = process_word(word)
        if len(res) > 1:
            results.add(res)

    results = [' - '.join(w) for w in results]
    results.sort()
    with open('results-{}.json'.format(args.limit), 'w') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)





    

