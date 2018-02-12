# Hungarian word list

This repository contains hungarian words in JSON formats separated by its class. The words are collected from [Wiktionary - Wiki Szotar](https://hu.wiktionary.org/wiki/Kezd%C5%91lap). The starting point was the [word class page](https://hu.wiktionary.org/wiki/Kateg%C3%B3ria:Sz%C3%B3fajok). The scraper algorithm was given with the related hungarian main classes by hand, then it parsed through the subsequnt pages according to the available links.

After the scraping, the words were saved in JSON format to separate files, then a custom algorithm searched for _anagrams_ in the files, and saved the result too.

| Word class  | Word count | Starting page |
| ----------- | :--------: | ------------- |
| foldrajzi nevek  | 4745  | [Wiktionary link](https://hu.wiktionary.org/wiki/Kateg%C3%B3ria:magyar_f%C3%B6ldrajzi_nevek) |
| fonevek  | 33969 | [Wiktionary link](https://hu.wiktionary.org/wiki/Kateg%C3%B3ria:magyar_f%C5%91nevek) |
| tobbes szamu alakok | 7380 | [Wiktionary link](https://hu.wiktionary.org/wiki/Kateg%C3%B3ria:magyar_t%C3%B6bbes_sz%C3%A1m%C3%BA_alakok) |
| hatarozoszok | 1205 | [Wiktionary link](https://hu.wiktionary.org/wiki/Kateg%C3%B3ria:magyar_hat%C3%A1roz%C3%B3sz%C3%B3k) |
| igek | 9264 | [Wiktionary link](https://hu.wiktionary.org/wiki/Kateg%C3%B3ria:magyar_ig%C3%A9k) |
| indulatszavak | 22 | [Wiktionary link](https://hu.wiktionary.org/wiki/Kateg%C3%B3ria:magyar_indulatsz%C3%B3k) |
| kotoszavak | 78 | [Wiktionary link](https://hu.wiktionary.org/wiki/Kateg%C3%B3ria:magyar_k%C3%B6t%C5%91sz%C3%B3k) |
| melleknevek | 9626 | [Wiktionary link](https://hu.wiktionary.org/wiki/Kateg%C3%B3ria:magyar_mell%C3%A9knevek) |
| mondatszavak | 64 | [Wiktionary link](https://hu.wiktionary.org/wiki/Kateg%C3%B3ria:magyar_mondatsz%C3%B3k) |
| nevmasok | 189 | [Wiktionary link](https://hu.wiktionary.org/wiki/Kateg%C3%B3ria:magyar_n%C3%A9vm%C3%A1sok) |
| nevutok | 27 | [Wiktionary link](https://hu.wiktionary.org/wiki/Kateg%C3%B3ria:magyar_n%C3%A9vut%C3%B3k) |
| szamnevek | 1805 | [Wiktionary link](https://hu.wiktionary.org/wiki/Kateg%C3%B3ria:magyar_sz%C3%A1mnevek) |
| tulajdonnevek | 3803 | [Wiktionary link](https://hu.wiktionary.org/wiki/Kateg%C3%B3ria:magyar_tulajdonnevek) |

All JSON files were encoded with __UTF-8__.


# License

The whole repo is available under __Creative Commons ShareAlike 3.0__ (CC BY-SA 3.0) as the source is released under the same license.
