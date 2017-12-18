import re
import sys
import argparse
from yelp_uri.encoding import recode_uri
from urllib.request import urlopen
from bs4 import BeautifulSoup

oropuare = "aāeēiīoōuū"
orokati = "hkmnprtwŋƒ"
pūriki_pākehā = "bcdfgjlqsvxyz'"
no_tohutō = ''.maketrans({'ā': 'a', 'ē': 'e', 'ī': 'i', 'ō': 'o', 'ū': 'u'})
arapū = "AaĀāEeĒēIiĪīOoŌōUuŪūHhKkMmNnPpRrTtWwŊŋƑƒ-"


def nahanaha(raupapa_māori):
    # Takes a word count dictionary (e.g. output of kōmiri_kupu) and returns the
    # list of Māori words in alphabetical order
    return sorted(raupapa_māori.keys(), key=lambda kupu: [arapū.index(pūriki) for pūriki in kupu])


def kōmiri_kupu(kupu_tōkau, kūare_tohutō=True):
    # Removes words that contain any English characters from the string above
    # Set kūare_tohutō=True to become sensitive to the presence of macrons when making the match

    # Splits the raw text along characters that a
    kupu_hou = re.findall('(?!-)(?!{p}*--{p}*)({p}+)(?<!-)'.format(
        p='[a-zāēīōū\-’\']'), kupu_tōkau, flags=re.IGNORECASE)

    # Reads the file lists of English and ambiguous words into list variables
    kōnae_pākehā, kōnae_rangirua = open("kupu_kino.txt" if kūare_tohutō else "kupu_kino_no_tohutō.txt", "r"), open(
        "kupu_rangirua.txt" if kūare_tohutō else "kupu_rangirua_no_tohutō.txt", "r")
    kupu_pākehā, kupu_rangirua = kōnae_pākehā.read(
    ).split(), kōnae_rangirua.read().split()
    kōnae_pākehā.close(), kōnae_rangirua.close()

    # Setting up the dictionaries in which the words in the text will be placed
    raupapa_māori, raupapa_rangirua, raupapa_pākehā = {}, {}, {}

    # Replaces ng and wh, w', w’ with ŋ and ƒ respectively, since Māori
    # consonants are easier to deal with in unicode format
    kupu_hou = [re.sub(r'w\'', 'ƒ', re.sub(r'w’', 'ƒ', re.sub(
        r'ng', 'ŋ', re.sub(r'wh', 'ƒ', kupu)))) for kupu in kupu_hou.lower]
    kupu_pākehā = [re.sub(r'w\'', 'ƒ', re.sub(r'w’', 'ƒ', re.sub(
        r'ng', 'ŋ', re.sub(r'wh', 'ƒ', kupu)))) for kupu in kupu_pākehā]
    kupu_rangirua = [re.sub(r'w\'', 'ƒ', re.sub(r'w’', 'ƒ', re.sub(
        r'ng', 'ŋ', re.sub(r'wh', 'ƒ', kupu)))) for kupu in kupu_rangirua]

    # Puts each word through tests to determine which word frequency dictionary
    # it should be referred to. Goes to the ambiguous dictionary if it's in the
    # ambiguous list, goes to the Māori dictionary if it doesn't have consecutive
    # consonants, doesn't end in a consnant, doesn't have any english letters
    # and isn't one of the provided stop words. Otherwise it goes to the non-Māori
    # dictionary. If this word hasn't been added to the dictionary, it does so,
    # and adds a count for every time the corresponding word gets passed to the
    # dictionary.

    for kupu in kupu_hou:
        if kupu in kupu_rangirua:
            kupu = re.sub(r'ŋ', 'ng', re.sub(r'ƒ', 'wh', kupu))
            if kupu not in raupapa_rangirua:
                raupapa_rangirua[kupu] = 0
            raupapa_rangirua[kupu] += 1
            continue
        elif not (re.compile("[{o}][{o}]".format(o=orokati)).search(kupu.lower()) or (kupu[-1].lower() in orokati) or any(pūriki in kupu.lower() for pūriki in pūriki_pākehā) or (kupu.lower() in kupu_pākehā)):
            kupu = re.sub(r'ŋ', 'ng', re.sub(r'ƒ', 'wh', kupu))
            if kupu not in raupapa_māori:
                raupapa_māori[kupu] = 0
            raupapa_māori[kupu] += 1
            continue
        else:
            kupu = re.sub(r'ŋ', 'ng', re.sub(r'ƒ', 'wh', kupu.lower()))
            if kupu not in raupapa_pākehā:
                raupapa_pākehā[kupu] = 0
            raupapa_pākehā[kupu] += 1

    return raupapa_māori, raupapa_rangirua, raupapa_pākehā


def hihira_raupapa_kupu(kupu_hou, kūare_tohutō=True):
    # Looks up a single word to see if it is defined in maoridictionary.co.nz
    # Set kūare_tohutō=False to not ignore macrons when making the match
    # Returns True or False

    kupu = kupu_hou.lower()
    if kūare_tohutō:
        kupu = kupu.translate(no_tohutō)
    taukaea = recode_uri(
        'http://maoridictionary.co.nz/search?idiom=&phrase=&proverb=&loan=&histLoanWords=&keywords=' + kupu)
    whārangi_ipurangi = urlopen(taukaea)
    hupa = BeautifulSoup(whārangi_ipurangi, 'html.parser',
                         from_encoding='utf8')

    tohu = hupa.find_all('h2')
    for taitara in tohu[:-3]:
        taitara = taitara.text.lower()
        if "found 0 matches" in taitara:
            return False
            break
        elif kupu in (taitara.translate(no_tohutō).split() if kūare_tohutō else taitara.split()):
            return True
            break
    return False


def hihira_raupapa(kupu_hou):
    # Looks up a list of words to see if they are defined in maoridictionary.co.nz
    # Set kūare_tohutō=False to become sensitive to the presence of macrons when making the match

    hihira = list(map(hihira_raupapa_kupu, kupu_hou))

    kupu_pai = [tokorua[1] for tokorua in zip(hihira, kupu_hou) if tokorua[0]]
    kupu_kino = [tokorua[1]
                 for tokorua in zip(hihira, kupu_hou) if not tokorua[0]]
    return kupu_pai, kupu_kino
