#! /usr/bin/python

import json
import sys

print('>> loading words..')
with open('words/words.json') as f:
    words = json.load(f)

print('>> {} words were loaded'.format(len(words)))

initials =  '0123456789'
initials += 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÖŐÜŰ'
initials += 'abcdefghijklmnopqrstuvwxyzáéíóúöőüű'

def log(count):
    sys.stdout.write('\r>> words to categorize: {:>6} '.format(count))
    sys.stdout.flush()

data = {}
count = len(words)
log(count)
for i in initials:
    temp_start = {}
    temp_valid = False
    for j in range(1, 90):
        temp_length = [w for w in words if w.startswith(i) and len(w) == j]
        if temp_length:
            temp_start[j] = temp_length
            words = [w for w in words if w not in temp_start[j]]
            count -= len(temp_start[j])
            temp_valid = True
            log(count)
    if temp_valid:
        data[i] = temp_start

print('\n>> {} words remained: {}'.format(count, words))

path = 'anagrams/search_dict.json'
print('>> writing {}'.format(path))
with open(path, 'w') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
print('>> done')
