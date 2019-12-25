# -*- coding: utf-8 -*-
'''Sample code with web scraping package beautifulsoup3

Get Japanese-English translator corpus from bible site.

(C) Tasuku Hori, exa Corporation Japan, 2017. all rights reserved.
'''

__author__ = 'Tasuku Hori'

import re
import os
import sys
import csv
import bs4
import random
import requests
from janome.tokenizer import Tokenizer

# Necessary packages:
#  pip install janome beautifulsoup4

class Bible():
    '''Load bible data from http://bible.e-lesson1.com/
    to build English Japanese corpus.
    '''
    DEFAULT_PATH = 'bible_utf8_unix.csv'

    def __init__(self, path=DEFAULT_PATH):
        '''If target path is not existed, load with the internet.
        '''
        self.path = path
        self.corpus = []
        try:
            if os.path.exists(path):
                print("Load from " + path)
                self.corpus = self.load_from_csv(path)
            else:
                print("Load from internet")
                self.corpus = self.load_from_net()
                self.save_to_csv(path, self.corpus)

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    def pray(self):
        '''if pray strictly, you will get shuffled corpus
        '''
        print("Shuffle corpus order")
        random.shuffle(self.corpus)

    @staticmethod
    def save_to_csv(path, data):
        '''save csv file with data.
        '''
        with open(path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(data)

    @staticmethod
    def load_from_csv(path):
        '''load from csv file to instance variable "corpus"
        '''
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            return [row for row in reader]

    @staticmethod
    def load_from_net():
        '''Load all bible data with the internet.
        '''
        result = []
        for url in Bible.url_iterator():
            result.extend(Bible._load_from_net(url))
        return result

    @staticmethod
    def _load_from_net(url):
        '''Load a selected
        '''
        print("target url: " + url)
        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.content, "html.parser")

        try:
            tables = soup.find("table", attrs={"border":"1", "style":"font-size : 10pt;line-height : 12pt;"})
            tds = tables.find_all("td")
        except:
            #print("font-size 9pt")
            tables = soup.find("table", attrs={"style":"font-size : 9pt;"})
            tds = tables.find_all("td")

        oneline = lambda td, sep: " ".join(td.strings).strip().replace('\r\n', sep)
        #return [[oneline(tds[ i * 3 + 1], ' '), Bible.wakati(oneline(tds[ i * 3 + 2], ''))] for i in range(int(len(tds) / 3))]
        result = []
        for i in range(len(tds) -1):
            first_text = oneline(tds[i], ' ')
            if re.match('[a-zA-Z_()]+', first_text):
                second_text = oneline(tds[i + 1], ' ')
                if re.match('[ぁ-んァ-ン一-龥]+', second_text):
                   result.append([first_text, Bible.wakati(second_text)])
        return result

    @staticmethod
    def wakati(sentence):
        '''Split wakati-gaki text with Japanese.
        '''
        malist = Tokenizer().tokenize(sentence)
        return " ". join([w.surface for w in malist]).strip()

    @staticmethod
    def url_iterator():
        '''target url iterator
        '''
        BASE_URL='http://bible.e-lesson1.com/'
        SECTIONS = [
                ['1', 'matthew', 28],
                ['1', 'mark', 16],
                ['1', 'luka', 24],
                ['1', 'john', 21],
                ['1', 'acts', 28],
                ['1', 'romans', 16],
                ['1', 'corinthians1-', 16],
                ['1', 'corinthians2-', 13],
                ['1', 'galatians', 6],
                ['1', 'ephesians', 6],
                ['1', 'philippians', 4],
                ['1', 'colossians', 4],
                ['1', 'thessalonians1-', 5],
                ['1', 'thessalonians2-', 3],
                ['1', 'timothy1-', 6],
                ['1', 'timothy2-', 4],
                ['1', 'titus', 3],
                ['1', 'philemon', 1],
                ['1', 'hebrews', 13],
                ['1', 'james', 5],
                ['1', 'peter1-', 5],
                ['1', 'peter2-', 3],
                ['1', 'john1-', 5],
                ['1', 'john2-', 1],
                ['1', 'john3-', 1],
                ['1', 'jude', 1],
                ['1', 'revelation', 22],
                ['2', 'genesis', 50],
                ['2', 'exodus', 40],
                ['2', 'leviticus', 27],
                ['2', 'numbers', 36],
                ['2', 'deuteronomy', 34],
                ['2', 'joshur', 24],
                ['2', 'judges', 21],
                ['2', 'ruth', 4],
                ['2', 'samuel1-', 31],
                ['2', 'samuel2-', 24],
                ['2', 'kings1-', 22],
                ['2', 'kings2-', 25],
                ['2', 'chronicles1-', 29],
                ['2', 'chronicles2-', 36],
                ['2', 'ezra', 10],
                ['2', 'nehemiah', 13],
                ['2', 'esther', 10],
                ['2', 'job', 42],
                ['2', 'psalms', 150],
                ['2', 'proverbs', 31],
                ['2', 'ecclesiastes', 12],
                ['2', 'songofsong', 8],
                ['2', 'isaiah', 66],
                ['2', 'jeremiah', 52],
                ['2', 'lamentations', 5],
                ['2', 'ezekiel', 48],
                ['2', 'daniel', 12],
                ['2', 'hosea', 14],
                ['2', 'joel', 3],
                ['2', 'amos', 9],
                ['2', 'obadiah', 1],
                ['2', 'jonah', 4],
                ['2', 'micah', 7],
                ['2', 'nahum', 3],
                ['2', 'habakkuk', 3],
                ['2', 'zephaniah', 2],
                ['2', 'zechariah', 14],
                ['2', 'malachi', 4]]

        for section in SECTIONS:
            for page in range(1, (section[2]+1)):
                if section[0] == '2' and section[1] == 'isaiah' and 20 < page and page < 26:
                    print("SKIPPED: " + BASE_URL + section[0] + section[1] + str(page) + ".htm")
                    continue
                if section[0] == '2' and section[1] == 'jeremiah' and 35 < page and page < 41:
                    print("SKIPPED: " + BASE_URL + section[0] + section[1] + str(page) + ".htm")
                    continue
                # added because of one line which japanese td-pair omitted
                #if section[0] == '2' and section[1] == 'chronicles1-' and 15 < page and page < 17:
                    #print("SKIPPED: " + BASE_URL + section[0] + section[1] + str(page) + ".htm")
                    #continue
                # added because of one line without hi-fn section element
                #if section[0] == '2' and section[1] == 'psalms' and page in PSALMS_NO_HEAD:
                    #print("SKIPPED: " + BASE_URL + section[0] + section[1] + str(page) + ".htm")
                    #continue

                yield BASE_URL + section[0] + section[1] + str(page) + ".htm"

def main():
    bible = Bible()
    bible.pray()
    resultNet = bible.corpus
    print("")
    print("Bible English-Japanese Copus data")
    print("Total:     " + str(len(resultNet)))
    print("File path: " + bible.path)
    print("")
    print("If you use on Windows, please run \"nkf -sW " + bible.path + " > bible_sjis_win.csv\"")
    print("")
if __name__ == '__main__':
    main()
