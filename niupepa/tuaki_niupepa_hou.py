# Collects all the text from Māori newspapers on nzdl.org

import csv
import re
import time
from pathlib import Path
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from datetime import datetime
from taumahi import *
from pandas import read_csv

pae_tukutuku = 'http://www.nzdl.org'
pae_tukutuku_haurua = '{}{}'.format(
    pae_tukutuku, '/gsdlmod?gg=text&e=p-00000-00---off-0niupepa--00-0----0-10-0---0---0direct-10---4-------0-1l--11-en-50---20-about---00-0-1-00-0-0-11-1-0utfZz-8-00-0-0-11-10-0utfZz-8-00&a=d&c=niupepa&cl=CL1')

niupepa_kōnae_ingoa = 'test.csv'
perehitanga_kōnae_ingoa = 'test2.csv'


def hihira_kuputohu_kōnae():
    # Checks if the urls and raw text have been collected, and if not it collects them.
    # Returns True/False
    if not Path(niupepa_kōnae_ingoa).exists():
        with open(niupepa_kōnae_ingoa, 'w') as kōnae:
            taukaea_kaituhi = csv.writer(kōnae)
            niupepa_taukaea_tūtira = tiki_niupepa_taukaea()
            taukaea_kaituhi.writerow(['newspaper', 'issue', 'link'])
            for pae in niupepa_taukaea_tūtira:
                perehitanga_ingoa_tūtira, taukaea_perehitanga_tūtira = tiki_perehitanga_taukaea(
                    pae)
                for perehitanga in zip(perehitanga_ingoa_tūtira, taukaea_perehitanga_tūtira):
                    taukaea_kaituhi.writerow(
                        [pae[0], perehitanga[0], perehitanga[1]])
            kōnae.close()
            print("\nCollected all URLs\n")

    if Path(perehitanga_kōnae_ingoa).exists():
        with open(perehitanga_kōnae_ingoa, 'r') as kōnae:
            # read all the lines
            # if there are as many data entries as there are newspaper issues:
                # print("\nThere is nothing to read, data is already up to date.\n")
                # return False
            # else:
            #     print("\nThe current text corpus is insufficient, rewriting file...\n")
            #     return True
            kōnae.close()
            print("\nThere is no current text corpus, collecting text...\n")
            return True
    else:
        print("\nThere is no current text corpus, collecting text...\n")
        return True


def tuhi_kupu_tōkau_kuputohu():
    # Writes raw text to a csv from the urls of newspaper issues
    with open(niupepa_kōnae_ingoa, 'r') as niupepa_kōnae, open(perehitanga_kōnae_ingoa, 'w') as perehitanga_kōnae:
        taukaea_kaituhi = csv.writer(perehitanga_kōnae)
        tuhinga = read_csv(niupepa_kōnae)
        niupepa_kōnae.close()
        # niupepa_ingoa_tūtira = tuhinga.newspapers
        # perehitanga_taukaea_tūtira = tuhinga.links
        for index, row in tuhinga.iterrows():
            print(list(row))
        csv.writer(perehitanga_kōnae).writerow(
            ['newspaper', 'issue', 'date_retrieved', 'percent māori', 'raw_text'])

        # for pae in zip(perehitanga_taukaea_tūtira, niupepa_ingoa_tūtira):
        #     perehitanga_tūtira = eval(pae[0])
        #     ingoa = pae[1]
        #     for takirua in perehitanga_tūtira:
        #         print("\nExtracting text from " + takirua[0] + " in " + ingoa)
        #         hupa = bs(urlopen(takirua[1]), 'html.parser')
        #         kupu_tōkau = hupa.select('div.documenttext')[0].find('td')
        #         if kupu_tōkau != None:
        #             if kupu_tōkau.text:
        #                 kupu = kupu_tōkau.text
        #                 print("Successfully extracted text from " +
        #                       takirua[0] + " in " + ingoa)
        #             else:
        #                 kupu = ''
        #                 print("Failed to extract text from " +
        #                       takirua[0] + " in " + ingoa)
        #         else:
        #             kupu = ''
        #             print("Failed to extract text from " +
        #                   takirua[0] + " in " + ingoa)
        #
        #         taukaea_kaituhi.writerow(
        #             [ingoa, takirua[0], datetime.now(), kupu])
        perehitanga_kōnae.close()


def tiki_niupepa_taukaea():
    # Collects the urls and names of all the newspapers
    hupa = bs(urlopen(pae_tukutuku_haurua), 'html.parser')

    taukaea_niupepa_tūtira = []
    niupepa_ingoa_tūtira = []

    print('\nChecking for newspapers\n')

    for td in hupa.select('div.top')[0].find_all('td', {"valign": "top"}):
        if td.a:
            taukaea_niupepa_tūtira += [pae_tukutuku + td.a['href']]
        elif td.text:
            tohu = td.text.strip()
            tohu = tohu[:tohu.index('1') - 1]
            niupepa_ingoa_tūtira += [tohu]
            print("Collected " + tohu)
        else:
            pass
    return list(zip(niupepa_ingoa_tūtira, taukaea_niupepa_tūtira))


def tiki_perehitanga_taukaea(niupepa_taukaea):
    # Collects the names and urls of each issue of a particular newspaper
    hupa = bs(urlopen(niupepa_taukaea[1]), 'html.parser')
    print("\nCollecting issues of " + niupepa_taukaea[0] + "\n")

    taukaea_perehitanga_tūtira = []
    perehitanga_ingoa_tūtira = []
    for td in hupa.select('#group_top')[0].find_all('td', {"valign": "top"}):
        if td.a:
            taukaea_perehitanga_tūtira += [pae_tukutuku + td.a['href']]
        elif td.text and ("No." in td.text or "Volume" in td.text) or ("1.27" in niupepa_taukaea[1] and "Commentary" in td.text):
            tohu = td.text.strip()
            if tohu == "Commentary":
                tohu = "No. 1"
            perehitanga_ingoa_tūtira += [tohu]
            print("Collected " + tohu)
        else:
            pass

    if taukaea_perehitanga_tūtira and perehitanga_ingoa_tūtira:
        print("\nCollected all issues of " + niupepa_taukaea[0] + "\n")
    else:
        print("\nDid not collect all issues of " + niupepa_taukaea[0] + "\n")

    return perehitanga_ingoa_tūtira, taukaea_perehitanga_tūtira


def matua():
    if hihira_kuputohu_kōnae():
        tuhi_kupu_tōkau_kuputohu()


if __name__ == '__main__':
    matua()

# tiki_perehitanga_taukaea(['Te Karere O Nui Tireni', 'http://www.nzdl.org/gsdlmod?gg=text&e=d-00000-00---off-0niupepa--00-0----0-10-0---0---0direct-10---4-------0-1l--11-en-50---20-about---00-0-1-00-0-0-11-1-0utfZz-8-00-0-0-11-10-0utfZz-8-00&a=d&c=niupepa&cl=CL1.1'])
