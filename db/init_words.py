import json

from tqdm import tqdm
from hashlib import md5


def generate_hash(filename):
    with open('{}.txt'.format(filename)) as input:
      with open('{}-md5.txt'.format(filename), 'w') as output:
        for line in input:
          value = line.rstrip()
          output.write(value)
          output.write('\t')
          output.write(md5(value.encode()).hexdigest())
          output.write('\n')


if __name__ == '__main__':
    with open('../words/words.json') as f:
        words = json.load(f)

    with open('_w.txt', 'w') as f:
        for word in tqdm(words):
            f.write(word)
            f.write('\t')
            f.write(md5(word.encode()).hexdigest())
            f.write('\n')

