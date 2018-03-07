import datetime
import json
import logging
import os
import requests
import sys
import time

from bs4 import BeautifulSoup
from multiprocessing import Pool, Manager
import queue


#=============================================================================
#  C O N F I G U R A T I O N

WORKER_COUNT = 256
WORKER_TIMEOUT = 10
OUTPUT_DIR = 'words'

SOURCE_HOST = 'https://hu.wiktionary.org'
SCRAPING_DATA = {
    'foldrajzi-nevek': '/wiki/Kateg%C3%B3ria:magyar_f%C3%B6ldrajzi_nevek',
    'fonevek': '/wiki/Kateg%C3%B3ria:magyar_f%C5%91nevek',
    'hatarozoszok': '/wiki/Kateg%C3%B3ria:magyar_hat%C3%A1roz%C3%B3sz%C3%B3k',
    'igek': '/wiki/Kateg%C3%B3ria:magyar_ig%C3%A9k',
    'indulatszok': '/wiki/Kateg%C3%B3ria:magyar_indulatsz%C3%B3k',
    'kotoszavak': '/wiki/Kateg%C3%B3ria:magyar_k%C3%B6t%C5%91sz%C3%B3k',
    'melleknevek': '/wiki/Kateg%C3%B3ria:magyar_mell%C3%A9knevek',
    'mondatszavak': '/wiki/Kateg%C3%B3ria:magyar_mondatsz%C3%B3k',
    'nevmasok': '/wiki/Kateg%C3%B3ria:magyar_n%C3%A9vm%C3%A1sok',
    'nevutok': '/wiki/Kateg%C3%B3ria:magyar_n%C3%A9vut%C3%B3k',
    'szamnevek': '/wiki/Kateg%C3%B3ria:magyar_sz%C3%A1mnevek',
    'tulajdonnevek': '/wiki/Kateg%C3%B3ria:magyar_tulajdonnevek',
    'tobbes-szamu-alakok': '/wiki/Kateg%C3%B3ria:magyar_t%C3%B6bbes_sz%C3%A1m%C3%BA_alakok'
}


#=============================================================================
#  U T I L S

def format_url(url):
    return SOURCE_HOST + url


#=============================================================================
#  W O R K E R S

def worker(params):
    q = params['queue']
    worker_id = params['id']
    data = {}

    logger = logging.getLogger('worker-{:03}'.format(worker_id))

    session = 0

    while True:
        session_id = '[{:03}:{:03}]'.format(worker_id, session)

        try:
            job = q.get(timeout=WORKER_TIMEOUT)
        except queue.Empty as e:
            logger.info('{} >>>> NOTHING TO DO <<<<'.format(session_id))
            return data

        category = job['category']
        url = job['url']

        if category not in data:
            data[category] = []

        logger.info('{} scraping {}'.format(session_id, category))

        new_jobs, word_count = execute_job(category, url, data[category])
        for new_job in new_jobs:
            q.put(new_job)

        logger.info('{} scraped {} words'.format(session_id, word_count))

        if len(new_jobs):
            logger.info('{} queued {} new jobs'.format(session_id, len(new_jobs)))

        session += 1

    return data


def execute_job(category, url, data):
    r = requests.get(url)
    additional_urls, word_count = parse_data(r.text, data)
    new_jobs = [{'category': category, 'url': format_url(url)} for url in additional_urls]
    return new_jobs, word_count


def parse_data(raw_data, data):
    soup = BeautifulSoup(raw_data, 'html.parser')
    urls = set()

    if soup.find(id='mw-subcategories'):
        for subcategory in soup.find(id='mw-subcategories').find_all('li'):
            suburl = subcategory.find('a')['href']
            urls.add(suburl)

    word_count = 0
    pages = soup.find(id='mw-pages')
    if pages:
        for li in pages.find_all('li'):
            word = li.a.string
            if word == 'magyar szótár':
                break
            if word != 'magyar főnévi alakok':
                data.append(word.encode())
                word_count += 1

    next_url = soup.find('a', string='következő oldal')
    if next_url:
        urls.add(next_url['href'])

    return urls, word_count


#=============================================================================
#  L O G G I N G

def init_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(name)11s | %(message)s')


#=============================================================================
#  P O O L

def get_pool(worker_count):
    logger = logging.getLogger('pool')
    pool = Pool(worker_count)
    logger.info('pool initialized with {} workers'.format(worker_count))
    return pool


#=============================================================================
#  Q U E U E

def get_queue():
    logger = logging.getLogger('queue')
    manager = Manager()
    q = manager.Queue()
    prefill_queue(q)
    logger.info('queue initialized and prefilled with {} jobs'.format(q.qsize()))
    return q

def prefill_queue(q):
    for category, url in SCRAPING_DATA.items():
        q.put({
            'category': category,
            'url': format_url(url)})


#=============================================================================
#  S C R A P I N G

def scrape(data, pool, queue, worker_count=10):
    logger = logging.getLogger('scraper')
    logger.info('scraping started')

    STARTED = time.time()

    params = [{'queue': queue, 'id': i} for i in range(worker_count)]
    for d in pool.imap(worker, params):
        for key, words in d.items():
            if key not in data:
                data[key] = []
            data[key] += words

    FINISHED = time.time()

    logger.info('finished in {0:.2f} seconds'.format(FINISHED - STARTED))


#=============================================================================
#  P O S T   P R O C E S S I N G

def filter_and_save_data(data):
    for category, words in data.items():
        words = [w.decode() for w in words]
        words = sorted(list(set(words)))
        save_words(category, words)


def save_words(category, words):
    logger = logging.getLogger('saver')
    path = os.path.join(OUTPUT_DIR, '{}.json'.format(category))
    with open(path, 'w') as f:
        json.dump(words, f, indent=4, ensure_ascii=False)
        logger.info('{:>32} | {:>5} | {:.2f}K'.format(path, len(words), os.path.getsize(path)/1024.0))


#=============================================================================
#  M A I N

def main():
    init_logging()
    logger = logging.getLogger('main')
    logger.info('started')

    STARTED = time.time()

    data = {}
    pool = get_pool(WORKER_COUNT)
    queue = get_queue()

    scrape(data, pool, queue, WORKER_COUNT)

    logger.info('post processing started')
    filter_and_save_data(data)

    FINISHED = time.time()
    logger.info('finished in {0:.2f} seconds'.format(FINISHED - STARTED))


if __name__ == '__main__':
    main()

