import re
import os
import sys
import argparse
from yelp_uri.encoding import recode_uri
from urllib.request import urlopen
from bs4 import BeautifulSoup

oropuare = "aāeēiīoōuū"
orokati = "hkmnprtwŋƒ"
no_tohutō = ''.maketrans({'ā': 'a', 'ē': 'e', 'ī': 'i', 'ō': 'o', 'ū': 'u'})
arapū = "AaĀāEeĒēIiĪīOoŌōUuŪūHhKkMmNnPpRrTtWwŊŋƑƒ-"


def nahanaha(raupapa_māori):
    # Takes a word count dictionary (e.g. output of kōmiri_kupu) and returns the
    # list of Māori words in alphabetical order
    tūtira = hōputu(raupapa_māori)
    tūtira = sorted(tūtira, key=lambda kupu: [arapū.index(
        pūriki) if pūriki in arapū else len(arapū) + 1 for pūriki in kupu])
    return hōputu(tūtira, False)


def hōputu(kupu, hōputu_takitahi=True):
    # Replaces ng and wh, w', w’ with ŋ and ƒ respectively, since Māori
    # consonants are easier to deal with in unicode format
    # The Boolean variable determines whether it's encoding or decoding
    # (set False if decoding)
    if isinstance(kupu, list):
        if hōputu_takitahi:
            return [re.sub(r'(w\')|(w’)|(wh)|(ng)|(W\')|(W’)|(Wh)|(Ng)|(WH)|(NG)', whakatakitahi, whakatomo) for whakatomo in kupu]
        else:
            return [re.sub(r'(ŋ)|(ƒ)|(Ŋ)|(Ƒ)', whakatakirua, whakatomo) for whakatomo in kupu]
    elif isinstance(kupu, dict):
        if hōputu_takitahi:
            return [re.sub(r'(w\')|(w’)|(wh)|(ng)|(W\')|(W’)|(Wh)|(Ng)|(WH)|(NG)', whakatakitahi, whakatomo) for whakatomo in kupu.keys()]
        else:
            return [re.sub(r'(ŋ)|(ƒ)|(Ŋ)|(Ƒ)', whakatakirua, whakatomo) for whakatomo in kupu.keys()]
    else:
        if hōputu_takitahi:
            return re.sub(r'(w\')|(w’)|(wh)|(ng)|(W\')|(W’)|(Wh)|(Ng)|(WH)|(NG)', whakatakitahi, kupu)
        else:
            return re.sub(r'(ŋ)|(ƒ)|(Ŋ)|(Ƒ)', whakatakirua, kupu)


def whakatakitahi(tauriterite):
    # If passed the appropriate letters, return the corresponding symbol
    oro = tauriterite.group(0)
    if oro == 'ng':
        return 'ŋ'
    elif oro == 'w\'' or oro == 'w’' or oro == 'wh':
        return 'ƒ'
    elif oro == 'Ng' or oro == 'NG':
        return 'Ŋ'
    else:
        return 'Ƒ'


def whakatakirua(tauriterite):
    # If passed the appropriate symbol, return the corresponding letters
    oro = tauriterite.group(0)
    if oro == 'ŋ':
        return 'ng'
    elif oro == 'ƒ':
        return 'wh'
    elif oro == 'Ŋ':
        return 'Ng'
    else:
        return 'Wh'


# Keys to the kupu_list dictionary:
keys = ['pākehā', 'rangirua', 'pākehā_kūare_tohutō', 'rangirua_kūare_tohutō']
kupu_lists = {}


def kōmiri_kupu(kupu_tōkau, tohutō=True):
    # Removes words that contain any English characters from the string above,
    # returns dictionaries of word counts for three categories of Māori words:
    # Māori, ambiguous, non-Māori (Pākehā)
    # Set tohutō = True to become sensitive to the presence of macrons when making the match

    # Splits the raw text along characters that a
    kupu_hou = re.findall('(?!-)(?!{p}*--{p}*)({p}+)(?<!-)'.format(
        p='[a-zāēīōū\-’\']'), kupu_tōkau, flags=re.IGNORECASE)

    # Gets the preferred word lists from the preloaded files
    kupu_rangirua = kupu_lists[keys[1]
                               ] if tohutō else kupu_lists[keys[3]]
    kupu_pākehā = kupu_lists[keys[0]
                             ] if tohutō else kupu_lists[keys[2]]
    kupu_hou = hōputu(kupu_hou)

    # Setting up the dictionaries in which the words in the text will be placed
    raupapa_māori, raupapa_rangirua, raupapa_pākehā = {}, {}, {}

    # Puts each word through tests to determine which word frequency dictionary
    # it should be referred to. Goes to the ambiguous dictionary if it's in the
    # ambiguous list, goes to the Māori dictionary if it doesn't have consecutive
    # consonants, doesn't end in a consnant, doesn't have any english letters
    # and isn't one of the provided stop words. Otherwise it goes to the non-Māori
    # dictionary. If this word hasn't been added to the dictionary, it does so,
    # and adds a count for every time the corresponding word gets passed to the
    # dictionary.

    for kupu in kupu_hou:
        if (kupu.lower() or kupu.lower().translate(tūare_tohutō)) in kupu_rangirua:
            kupu = hōputu(kupu, False)
            if kupu not in raupapa_rangirua:
                raupapa_rangirua[kupu] = 0
            raupapa_rangirua[kupu] += 1
            continue
        elif not (re.compile("[{o}][{o}]".format(o=orokati)).search(kupu.lower()) or (kupu[-1].lower() in orokati) or any(pūriki not in arapū for pūriki in kupu.lower()) or ((kupu.lower() or whakatakitahi_oropuare(kupu)) in kupu_pākehā)) or len(kupu) == 1:
            kupu = hōputu(kupu, False)
            if kupu not in raupapa_māori:
                raupapa_māori[kupu] = 0
            raupapa_māori[kupu] += 1
            continue
        else:
            kupu = hōputu(kupu, False)
            if kupu not in raupapa_pākehā:
                raupapa_pākehā[kupu] = 0
            raupapa_pākehā[kupu] += 1

    return raupapa_māori, raupapa_rangirua, raupapa_pākehā


def whakatakitahi_oropuare(kupu):
    return re.sub(r'uu', 'u', re.sub(r'oo', 'o', re.sub(r'ii', 'i', re.sub(r'ee', 'e', re.sub(r'aa', 'a', kupu)))))


def hihira_raupapa_kupu(kupu_hou, tohutō):
    # Looks up a single word to see if it is defined in maoridictionary.co.nz
    # Set tohutō = False to not ignore macrons when making the match
    # Returns True or False

    kupu_huarua = kupu_hou.lower()
    if tohutō:
        kupu_huarua = kupu_huarua.translate(no_tohutō)
    taurua = [kupu_huarua, whakatakitahi_oropuare(kupu_huarua)]
    wāriutanga = False

    for kupu in taurua:
        taukaea = recode_uri(
            'http://maoridictionary.co.nz/search?idiom=&phrase=&proverb=&loan=&histLoanWords=&keywords=' + kupu)
        hupa = BeautifulSoup(urlopen(taukaea), 'html.parser',
                             from_encoding='utf8')

        tohu = hupa.find_all('h2')

        for taitara in tohu[:-2]:
            taitara = taitara.text.lower()
            if kupu in (taitara.translate(no_tohutō).split() if tohutō else taitara.split()):
                wāriutanga = True
                break
            else:
                pass

    print("Found " + kupu + ": " + str(wāriutanga))
    return wāriutanga


def hihira_raupapa(kupu_hou, tohutō=False):
    # Looks up a list of words to see if they are defined in maoridictionary.co.nz
    # Set tohutō = False to become sensitive to the presence of macrons when making the match

    hihira = [hihira_raupapa_kupu(kupu, tohutō) for kupu in kupu_hou]

    kupu_pai = [tokorua[1] for tokorua in zip(hihira, kupu_hou) if tokorua[0]]
    kupu_kino = [tokorua[1]
                 for tokorua in zip(hihira, kupu_hou) if not tokorua[0]]
    return kupu_pai, kupu_kino


def kupu_ratios(text, tohutō=True):
    map_Māori, map_ambiguous, map_other = kōmiri_kupu(text, tohutō)

    num_Māori = sum(map_Māori.values())
    num_ambiguous = sum(map_ambiguous.values())
    num_other = sum(map_other.values())

    heMāori = get_percentage(num_Māori, num_ambiguous, num_other)
    save_corpus = heMāori > 50

    return save_corpus, [num_Māori, num_ambiguous, num_other, heMāori]


def get_percentage(num_Māori, num_ambiguous, num_other):
    if num_Māori:
        return round(100 * num_Māori / (num_Māori + num_other), 2)
    elif num_other or num_ambiguous <= 10:
        return 0
    else:
        return 51


def auaha_raupapa_tū(kupu_tōkau, tohutō=True):
    # Removes words that contain any English characters from the string above,
    # returns dictionaries of word counts for three categories of Māori words:
    # Māori, ambiguous, non-Māori (Pākehā)
    # Set tohutō = True to become sensitive to the presence of macrons when making the match

    # Splits the raw text along characters that a
    kupu_hou = re.findall('(?!-)(?!{p}*--{p}*)({p}+)(?<!-)'.format(
        p='[a-zāēīōū\-’\']'), kupu_tōkau, flags=re.IGNORECASE)

    # Setting up the dictionaries in which the words in the text will be placed
    raupapa_māori, raupapa_pākehā = {}, {}

    kupu_hou = hōputu(kupu_hou)

    # Puts each word through tests to determine which word frequency dictionary
    # it should be referred to. Goes to the Māori dictionary if it doesn't have
    # consecutive consonants, doesn't end in a consnant, or doesn't have any
    # English letters. Otherwise it goes to the non-Māori dictionary. If this
    # word hasn't been added to the dictionary, it does so, and adds a count for
    # every time the corresponding word gets passed to the dictionary.

    for kupu in kupu_hou:
        if not (re.compile("[{o}][{o}]".format(o=orokati)).search(kupu.lower()) or (kupu[-1].lower() in orokati) or any(pūriki not in arapū for pūriki in kupu.lower())):
            kupu = hōputu(kupu, False)
            if kupu not in raupapa_māori:
                raupapa_māori[kupu] = 0
            raupapa_māori[kupu] += 1
            continue
        else:
            kupu = hōputu(kupu, False)
            if kupu not in raupapa_pākehā:
                raupapa_pākehā[kupu] = 0
            raupapa_pākehā[kupu] += 1

    return raupapa_māori, raupapa_pākehā


try:
    root = __file__
    if os.path.islink(root):
        root = os.path.realpath(root)
    dirpath = os.path.dirname(os.path.abspath(root)) + '/taumahi_tūtira'

    # Reads the file lists of English and ambiguous words into list variables
    filenames = ["/kupu_kino.txt", "/kupu_rangirua.txt",
                 "/kupu_kino_kūare_tohutō.txt", "/kupu_rangirua_kūare_tohutō.txt"]
    for pair in zip(keys, filenames):
        with open(dirpath + pair[1], "r") as kōnae:
            kupu_lists[pair[0]] = hōputu(kōnae.read().split())
except Exception as e:
    print(e)
    print("I'm sorry, but something is wrong.")
    print("There is no __file__ variable. Please contact the author.")
    sys.exit()


# All following script is for cleaning raw text strings:

apostrophes = '‘’\''
sentence_end = ['[.!?]', '[{}]*'.format(apostrophes)]

# Regex for detecting the end of a paragraph and beginning of another
new_paragraph = re.compile(
    '({}+|-+){}\n'.format(sentence_end[0], sentence_end[1]))

# Regex to detect the end of a sentence
new_sentence = re.compile('{}{} '.format(sentence_end[0], sentence_end[1]))


def clean_whitespace(paragraph):
    return re.sub(r'\s+', ' ', paragraph).strip()


# Regex to replace all tilda_vowels with macron vowels
vowel_map = {'a': 'ā', 'e': 'ē', 'i': 'ī', 'o': 'ō', 'u': 'ū'}
vowels = re.compile(r'(A?~|\[A macron\])([aeiouAEIOU])')


def sub_vowels(txt):
    return vowels.sub(tilda2tohutō, txt)
