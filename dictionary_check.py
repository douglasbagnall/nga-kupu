#checks words that are considered 'māori' against māoridictionary.co.nz to determine whether they are legitimate words
import re
from urllib.request import urlopen
from yelp_uri.encoding import recode_uri
from bs4 import BeautifulSoup
import sys

no_tohutō = ''.maketrans({'ā':'a', 'ē':'e', 'ī':'i', 'ō':'o', 'ū':'u'})

def dictionary_check_word(kupu_hou, ignore_tohutō=False):
    # Looks up a single word to see if it is defined in maoridictionary.com
    # Set ignore_tohutō=True to igbnore macrons when making the match
    # Returns True or False

    kupu = kupu_hou.lower()
    if ignore_tohutō:
        kupu = kupu.translate(no_tohutō)
    search_page = 'http://maoridictionary.co.nz/search?idiom=&phrase=&proverb=&loan=&histLoanWords=&keywords=' + kupu
    search_page = recode_uri(search_page)
    page = urlopen(search_page)
    soup = BeautifulSoup(page, 'html.parser', from_encoding='utf8')

    titles = soup.find_all('h2')
    for title in titles[:-3]:
        if "Found 0 matches" in title.text:
            return False
            break
        elif kupu in (title.text.translate(no_tohutō) if ignore_tohutō else title.text):
            return True
            break
    return False


def dictionary_check(kupu_hou):
    #looks up a list of words to see if they are defined in maoridictionary.com

    checks = list(map(dictionary_check_word, kupu_hou))
    good_list =  [pair[1] for pair in zip(checks, kupu_hou) if pair[0]]
    bad_list  =  [pair[1] for pair in zip(checks, kupu_hou) if not pair[0]]
    return good_list, bad_list


