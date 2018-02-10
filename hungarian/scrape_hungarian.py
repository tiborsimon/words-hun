import datetime
import json
import os
import requests
import sys
import time

from bs4 import BeautifulSoup


OUTPUT_FILE_NAME = "hungarian.json"
STATUS_FILE_NAME = "hungarian-last-execution.txt"
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

STATISTICS = {
    'rest_requests': 0,
    'downloaded_data': 0,
    'start_time': time.time()
}


def scrape():
    # import pudb; pudb.set_trace()
    data_dict = {}
    for category, url in SCRAPING_DATA.items():
        data = []
        urls = set([url])
        while urls:
            next_link = SOURCE_HOST + urls.pop()
            r = requests.get(next_link)
            STATISTICS['rest_requests'] += 1
            STATISTICS['downloaded_data'] += len(r.content)
            parse_data(r.text, data, urls)
            sys.stdout.write('    {}:{}{}\r'.format(category, ' '*(20-len(category)), len(data)))
            sys.stdout.flush()
        data_dict[category] = sorted(list(set(data)))
        print('')
    return data_dict


def parse_data(raw_data, data, urls):
    soup = BeautifulSoup(raw_data, 'html.parser')

    if soup.find(id='mw-subcategories'):
        for subcategory in soup.find(id='mw-subcategories').find_all('li'):
            suburl = subcategory.find('a')['href']
            urls.add(suburl)

    pages = soup.find(id='mw-pages')
    if pages:
        for li in pages.find_all('li'):
            word = li.a.string
            if word == 'magyar szótár':
                break
            if word != 'magyar főnévi alakok':
                data.append(word)
    next_url = soup.find('a', string='következő oldal')
    if next_url:
        urls.add(next_url['href'])


def print_result(data):
    count = 0
    for _,d in data.items():
        count += len(d)
    status = 'Latest execution at {}\n\n'.format(datetime.datetime.now())
    status += '    Word count:          {}\n'.format(count)
    status += '    REST requests:       {}\n'.format(STATISTICS['rest_requests'])
    status += '    Data downloaded:     {0:.2f} MB\n'.format(STATISTICS['downloaded_data']/1024/1024.0)
    status += '    JSON file size:      {0:.2f} MB\n'.format(os.path.getsize(OUTPUT_FILE_NAME)/1024/1024.0)
    status += '    Execution time:      {0:.2f} s\n'.format(time.time() - STATISTICS['start_time'])
    print('')
    print(status)
    with open(STATUS_FILE_NAME, 'w') as f:
        f.write(status)


def save_data(data):
    with open(OUTPUT_FILE_NAME, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def main():
    print('Collecting all hungarian words from {}\n'.format(SOURCE_HOST))
    data = scrape()
    save_data(data)
    print_result(data)


if __name__ == '__main__':
    main()
