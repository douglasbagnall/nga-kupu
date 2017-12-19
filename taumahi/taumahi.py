import re
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
    tūtira = hōputu(raupapa_māori.keys())
    tūtira = sorted(tūtira, key=lambda kupu: [arapū.index(
        pūriki) if pūriki in arapū else len(pūriki) + 1 for pūriki in kupu])
    return hōputu(tūtira, True, False)


def hōputu(kupu, tūtira=True, hōputu_takitahi=True):
    # Replaces ng and wh, w', w’ with ŋ and ƒ respectively, since Māori
    # consonants are easier to deal with in unicode format
    # First Boolean variable determines whether it's been passed a list (set
    # False if string) so that it can return a list. The second Boolean variable
    # determines whether it's encoding or decoding (set False if decoding)
    if tūtira:
        if hōputu_takitahi:
            return [re.sub(r'(w\')|(w’)|(wh)|(ng)|(W\')|(W’)|(Wh)|(Ng)|(WH)|(NG)', whakatakitahi, whakatomo) for whakatomo in kupu]
        else:
            return [re.sub(r'(ŋ)|(ƒ)|(Ŋ)|(Ƒ)', whakatakirua, whakatomo) for whakatomo in kupu]
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


def kōmiri_kupu(kupu_tōkau, kūare_tohutō=True):
    # Removes words that contain any English characters from the string above,
    # returns dictionaries of word counts for three categories of Māori words:
    # Māori, ambiguous, non-Māori (Pākehā)
    # Set kūare_tohutō = True to become sensitive to the presence of macrons when making the match

    # Splits the raw text along characters that a
    kupu_hou = re.findall('(?!-)(?!{p}*--{p}*)({p}+)(?<!-)'.format(
        p='[a-zāēīōū\-’\']'), kupu_tōkau, flags=re.IGNORECASE)

    # Reads the file lists of English and ambiguous words into list variables
    kōnae_pākehā, kōnae_rangirua = open("kupu_kino.txt" if kūare_tohutō else "kupu_kino_no_tohutō.txt", "r"), open(
        "kupu_rangirua.txt" if kūare_tohutō else "kupu_rangirua_no_tohutō.txt", "r")
    kupu_pākehā = kōnae_pākehā.read().split()
    kupu_rangirua = kōnae_rangirua.read().split()
    kōnae_pākehā.close(), kōnae_rangirua.close()

    # Setting up the dictionaries in which the words in the text will be placed
    raupapa_māori, raupapa_rangirua, raupapa_pākehā = {}, {}, {}

    kupu_hou, kupu_pākehā, kupu_rangirua = hōputu(
        kupu_hou), hōputu(kupu_pākehā), hōputu(kupu_rangirua)

    # Puts each word through tests to determine which word frequency dictionary
    # it should be referred to. Goes to the ambiguous dictionary if it's in the
    # ambiguous list, goes to the Māori dictionary if it doesn't have consecutive
    # consonants, doesn't end in a consnant, doesn't have any english letters
    # and isn't one of the provided stop words. Otherwise it goes to the non-Māori
    # dictionary. If this word hasn't been added to the dictionary, it does so,
    # and adds a count for every time the corresponding word gets passed to the
    # dictionary.

    for kupu in kupu_hou:
        if kupu.lower() in kupu_rangirua:
            kupu = hōputu(kupu, False, False)
            if kupu not in raupapa_rangirua:
                raupapa_rangirua[kupu] = 0
            raupapa_rangirua[kupu] += 1
            continue
        elif not (re.compile("[{o}][{o}]".format(o=orokati)).search(kupu.lower()) or (kupu[-1].lower() in orokati) or any(pūriki not in arapū for pūriki in kupu.lower()) or (kupu.lower() in kupu_pākehā)):
            kupu = hōputu(kupu, False, False)
            if kupu not in raupapa_māori:
                raupapa_māori[kupu] = 0
            raupapa_māori[kupu] += 1
            continue
        else:
            kupu = hōputu(kupu, False, False)
            if kupu not in raupapa_pākehā:
                raupapa_pākehā[kupu] = 0
            raupapa_pākehā[kupu] += 1

    return raupapa_māori, raupapa_rangirua, raupapa_pākehā


def hihira_raupapa_kupu(kupu_hou, kūare_tohutō=True):
    # Looks up a single word to see if it is defined in maoridictionary.co.nz
    # Set kūare_tohutō = False to not ignore macrons when making the match
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
    # Set kūare_tohutō = False to become sensitive to the presence of macrons when making the match

    hihira = list(map(hihira_raupapa_kupu, kupu_hou))

    kupu_pai = [tokorua[1] for tokorua in zip(hihira, kupu_hou) if tokorua[0]]
    kupu_kino = [tokorua[1]
                 for tokorua in zip(hihira, kupu_hou) if not tokorua[0]]
    return kupu_pai, kupu_kino


def kupu_ratios(text):
    map_Māori, map_ambiguous, map_other = kōmiri_kupu(text)
    # ambiguous map may include words such as:
    # ['take', 'Take', 'too', 'Too', 'woo', 'hoo', 'No', 'no', 'Ha', 'ha', 'name', 'one', 'where', 'who', 'We', 'we', 'Nowhere', 'nowhere', 'are', 'he', 'hero', 'here', 'none', 'whoa']

    num_Māori = sum(map_Māori.values())
    num_ambiguous = sum(map_ambiguous.values())
    num_other = sum(map_other.values())

    heMāori = 0

    if num_Māori:
        heMāori = 100 * num_Māori / (num_Māori + num_other)
    elif num_other or num_ambiguous <= 10:
        heMāori = 0
    else:
        heMāori = 51

    save_corpus = heMāori > 50

    return save_corpus, [num_Māori, num_ambiguous, num_other, heMāori]
