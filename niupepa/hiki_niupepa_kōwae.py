# Collects all the text from Māori newspapers on nzdl.org

import csv
import re
import time
import argparse
from pathlib import Path
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from datetime import datetime
from taumahi import *

pae_tukutuku = 'http://www.nzdl.org'
pae_tukutuku_haurua = '{}{}'.format(
    pae_tukutuku, '/gsdlmod?gg=text&e=p-00000-00---off-0niupepa--00-0----0-10-0---0---0direct-10---4-------0-1l--11-en-50---20-about---00-0-1-00-0-0-11-1-0utfZz-8-00-0-0-11-10-0utfZz-8-00&a=d&c=niupepa&cl=CL1')

niupepa_kōnae_ingoa = 'niupepa_kuputohu.csv'
perehitanga_kōnae_ingoa = 'perehitanga_kuputohu.csv'


def hihira_niupepa_kuputohu(kōwhiri):
    # Checks if the urls and raw text have been collected, and if not it collects them.
    if not Path(kōwhiri.urlfile if kōwhiri.urlfile else niupepa_kōnae_ingoa).exists():
        # If there is not a current url file, it begins to write one
        with open(kōwhiri.urlfile if kōwhiri.urlfile else niupepa_kōnae_ingoa, 'w') as kōnae:
            taukaea_kaituhi = csv.writer(kōnae)
            niupepa_taukaea_tūtira = tiki_niupepa_taukaea()  # List of all the newspaper links
            taukaea_kaituhi.writerow(['newspaper', 'issue', 'link'])
            for pae in niupepa_taukaea_tūtira:
                # Gets a list of issue names and urls and loops through them
                perehitanga_tūtira = tiki_perehitanga_taukaea(pae)
                for perehitanga in perehitanga_tūtira:
                    taukaea_kaituhi.writerow(
                        [pae[0], perehitanga[0], perehitanga[1]])  # Writes the newspaper name, issue name, and issue url for every issue of every newspaper
            kōnae.close()
            print("\nCollected all URLs.\nCollecting text...\n")

    else:
        print("\nURLs are ready to be checked.\n")

    return


def tuhi_kupu_tōkau_kuputohu(kōwhiri, mātāmuri_rārangi=None):
    # Writes raw text to a csv from the urls of newspaper issues
    niupepa_kōnae = open(
        kōwhiri.urlfile if kōwhiri.urlfile else niupepa_kōnae_ingoa, 'r')
    # Reads the csv file of urls to a variable
    tuhinga = csv.reader(niupepa_kōnae)

    # Opens the file to write where
    perehitanga_kōnae = open(
        kōwhiri.textfile if kōwhiri.textfile else perehitanga_kōnae_ingoa, 'a')
    perehitanga_kaituhituhi = csv.writer(perehitanga_kōnae)

    if not mātāmuri_rārangi:  # If this is False, it means to start writing the file from scratch
        perehitanga_kaituhituhi.writerow(
            ['date_retrieved', 'newspaper', 'issue', 'page', 'percent_māori', 'raw_text', 'url'])  # Writes the column names since the file did not exist
    else:
        for kapa in tuhinga:  # Loops through each row in the url csv
            # When it reaches the issue it last pulled a page from
            if mātāmuri_rārangi[1:3] == kapa[0:2]:
                whārangi_tūtira = tiki_kupu_tōkau(
                    kapa, tiki_hupa_tūtira(kapa))

                for kuputohu in range(len(whārangi_tūtira)):
                    if whārangi_tūtira[kuputohu][0] == mātāmuri_rārangi[3]:
                        break

                whārangi_tūtira = whārangi_tūtira[kuputohu:]
                if kuputohu == -1:
                    print("\n-----Could not find the exact page in the existing document. Some of the rest of the issue's pages may have been skipped.-----\n")

                rāringa_kaituhituhi(
                    kapa, perehitanga_kaituhituhi, whārangi_tūtira)
                break
            else:
                pass

        # Loops through the existing rows until it gets to the previous url, then continues grabbing the text from the pages of that issue
        # Gets the text from all pages of the issues of the newspaper that the last url was found in
        rārangi_kuputohu = 0

    # Iterates through the url csv file, extracting newspaper name, issue name, and issue url
    for tōtoru in tuhinga:  # Iterates through each row in the document
        # Gets all the pages of a particular issue
        # Gets a tuple of the page's number, text and url
        whārangi_tūtira = tiki_kupu_tōkau(tōtoru, tiki_hupa_tūtira(tōtoru))
        rāringa_kaituhituhi(tōtoru, perehitanga_kaituhituhi, whārangi_tūtira)

    niupepa_kōnae.close()
    perehitanga_kōnae.close()
    return


def rāringa_kaituhituhi(tōtoru, kaituhituhi, kupu_kapa):
    # This function writes all the information to the text csv, i.e. date retrieved,
    # Newspaper name, issue name, page number, Māori percentage, page text, and
    # The page url. It takes a tuple, a csv writer, and a list. The tuple contains
    # The newspaper name, issue name and issue url. The list contains tuples of
    # Each page of the issue's page number, text and url. Only the page-specific
    # Url is used.

    for takitoru in kupu_kapa:  # Loops through pages in the list of tuples
        kupu_tōkau = re.sub(r'[ ]{2,}', r' ', re.sub(
            r'[\n]{2,}', '\n', takitoru[1].strip()))  # Cleans up excess spaces and new line characters
        # Gets the percentage of the text that is Māori
        ōrau = tiki_ōrau(kupu_tōkau)
        kaituhituhi.writerow(
            [datetime.now(), tōtoru[0], tōtoru[1], takitoru[0], ōrau, kupu_tōkau, takitoru[2]])  # Writes the date retrieved, newspaper name, issue name, page number, Māori percentage, extracted text and page url to the file


def tiki_hupa_tūtira(tōtoru):
    # This function checks to see if there are any links to following pages and
    # Returns a list of tuples containing the page number, html and url of each
    # Of these pages. Input is a tuple of newspaper name, issue name, issue url.
    print("\n\nCollecting pages of " + tōtoru[1] + " in " + tōtoru[0])
    # Extracts the soup of the first page
    whārangi_hupa = bs(urlopen(tōtoru[2]), 'html.parser')
    # Extracts the page number from the soup
    whārangi_tau = whārangi_hupa.find('b').text.split("page  ")[1]
    # Adds the page number and soup as a tuple as the first element of a list which will be used in tiki_kupu_tōkau
    hupa_tūtira = [(whārangi_tau, whārangi_hupa, tōtoru[2])]

    while True:
        taukaea_pinetohu = hupa_tūtira[-1][1].select('div.navarrowsbottom')[
            0].find('td', align='right', valign='top')  # Finds the next page button of the current soup
        if taukaea_pinetohu.a == None:
            # If there is no next page button, the process ends and the list is returned
            return hupa_tūtira
        elif taukaea_pinetohu.a['href']:
            # If there is a link, its page number, soup and url are added as a tuple to the list
            hupa_tūtira += [(taukaea_pinetohu.text.strip(), bs(
                urlopen(pae_tukutuku + taukaea_pinetohu.a['href']), 'html.parser'), pae_tukutuku + taukaea_pinetohu.a['href'])]
        else:
            print("\nError collecting all pages\n")
            return hupa_tūtira  # If there is an error the list is returned early


def tiki_kupu_tōkau(tōtoru, hupa_tūtira):
    # Extracts the text for all pages of the issue it has been passed.
    # It takes a tuple and a list. The tuple has the newspaper name, issue name
    # And issue link. The list is of tuples containing each page of the issue's
    # Number, soup and url. It outputs a list of tuples, which contain each page
    # Of an issue's number, text and url.
    print("Extracting text from " + tōtoru[1] + " in " + tōtoru[0] + ":\n")
    whārangi_kupu = []  # Sets up list of tuples for the page number
    for hupa in hupa_tūtira:  # Loops through each tuple in the tuple list
        kupu_tōkau = hupa[1].select('div.documenttext')[
            0].find('td')  # Simplifies the soup
        if kupu_tōkau != None:
            if kupu_tōkau.text:
                # Adds the page number and extracted text as a tuple to the list, if the text exists
                whārangi_kupu += [(hupa[0], kupu_tōkau.text, hupa[2])]
                print("Extracted text from page " + hupa[0])
            else:
                print("Failed to extract text from page " + hupa[0] + " of " +
                      tōtoru[1] + " in " + tōtoru[0])  # If there is no text found, print an error
        else:
            print("Failed to extract text from page " + hupa[0] + " of " +
                  tōtoru[1] + " in " + tōtoru[0])

    print("\nFinished with " + tōtoru[1] + " in " + tōtoru[0])
    return whārangi_kupu


def tiki_niupepa_taukaea():
    # Collects the urls and names of all the newspapers
    # Opens the archive page and fetches the soup
    hupa = bs(urlopen(pae_tukutuku_haurua), 'html.parser')

    taukaea_niupepa_tūtira = []  # Sets up where the names and links will be stored
    niupepa_ingoa_tūtira = []

    print('\nChecking for newspapers\n')

    # Gets a list of all tags where newspaper links are stored
    for td in hupa.select('div.top')[0].find_all('td', {"valign": "top"}):
        if td.a:
            # If there is a link, adds it to the link list. the link will have the same index as its name in the corresponding list
            taukaea_niupepa_tūtira += [pae_tukutuku + td.a['href']]
        elif td.text:
            tohu = td.text.strip()
            tohu = tohu[:tohu.index(' (')]
            # If there is text, it will be a title. it strips off how many issues there are, which begins with ' (', and adds it to the name list.
            niupepa_ingoa_tūtira += [tohu]
            print("Collected " + tohu)
        else:
            pass
    # Makes a single list, elements are made into tuples and passed to a single list, then returned
    return list(zip(niupepa_ingoa_tūtira, taukaea_niupepa_tūtira))


def tiki_perehitanga_taukaea(niupepa_taukaea):
    # Collects the names and urls of each issue of a particular newspaper
    hupa = bs(urlopen(niupepa_taukaea[1]), 'html.parser')
    print("\nCollecting issues of " + niupepa_taukaea[0] + "\n")

    taukaea_perehitanga_tūtira = []  # Sets up empty lists which are to be added to
    perehitanga_ingoa_tūtira = []
    # Finds all tags that contain links and issue names
    for td in hupa.select('#group_top')[0].find_all('td', {"valign": "top"}):
        if td.a:
            # If there is a link, adds it to the link list. names and urls have the same index in their respective lists
            taukaea_perehitanga_tūtira += [pae_tukutuku + td.a['href']]
        elif td.text and ("No." in td.text or "Volume" in td.text) or ("1.27" in niupepa_taukaea[1] and "Commentary" in td.text):
            # Makes sure text meets criteria, as there is some unwanted text. the second bracket is a specific case that doesn't get picked up by the first bracket
            tohu = td.text.strip()
            if tohu == "Commentary":
                tohu = "No. 1"  # Manually renames the specific case, as it is too different from the other issue names to easily include in the loop
            # Adds the name to the name list
            perehitanga_ingoa_tūtira += [tohu]
            print("Collected " + tohu)
        else:
            pass

    # Prints a message to the terminal to determine errors
    if taukaea_perehitanga_tūtira and perehitanga_ingoa_tūtira:
        print("\nCollected issues of " + niupepa_taukaea[0] + "\n")
    else:
        print("\nDid not collect any issues of " + niupepa_taukaea[0] + "\n")

    # Zips the name and url lists together, returns
    return list(zip(perehitanga_ingoa_tūtira, taukaea_perehitanga_tūtira))


def tiki_ōrau(kōwae):
    # Uses the kōmiri_kupu function from the taumahi module to estimate how
    # Much of the text is Māori. Input is a string of text
    raupapa_māori, raupapa_rangirua, raupapa_pākehā = kōmiri_kupu(kōwae, False)

    tatau_māori = sum(raupapa_māori.values())
    tatau_pākehā = sum(raupapa_pākehā.values())
    tatau_tapeke = tatau_māori + tatau_pākehā

    if tatau_tapeke != 0:
        return "{:0.2f}%".format((tatau_māori / tatau_tapeke) * 100)
    else:
        return "0.00%"


def matua():

    # Starts recording the time to detail how long the entire process took
    tāti_wā = time.time()

    whakatukai = argparse.ArgumentParser()
    whakatukai.add_argument(
        '--urlfile', '-u', help="Intermediate csv file where the newspaper names, issue names, and issue urls are stored")
    whakatukai.add_argument(
        '--textfile', '-t', help="Output csv file where the date retrieved, newspaper names, issue names, page numbers, Māori percentage, page text and page urls are stored")
    kōwhiri = whakatukai.parse_args()

    # Checks whether url file exists, otherwise writes one
    hihira_niupepa_kuputohu(kōwhiri)

    if Path(perehitanga_kōnae_ingoa).exists():  # Checks whether there is a csv of the text
        with open(kōwhiri.textfile if kōwhiri.textfile else perehitanga_kōnae_ingoa, 'r') as kōnae:

            kupuhou_kōnae = csv.reader(kōnae)
            rārangi = None
            for rārangi in kupuhou_kōnae:
                pass

            # Gets the newspaper name, issue and page number of the last entry recorded
            mātāmuri_perehitanga = rārangi[1:4]

            if mātāmuri_perehitanga == ['Te Toa Takitini 1921-1932', 'Volume 1, No. 7', '96']:
                # If the last one is as below, the file is up to date.
                print("\nThere is nothing to read, data is already up to date.\n")
            else:
                print("\nThe current text corpus is insufficient, rewriting file...\n")
                # Otherwise, it passes where it was last up to to the text csv writer so it may continue from there
                tuhi_kupu_tōkau_kuputohu(kōwhiri, rārangi)
            kōnae.close()

    else:
        print("\nThere is no current text corpus, collecting text...\n")
        # If there is no text csv file, it begins to write one from scratch
        tuhi_kupu_tōkau_kuputohu(kōwhiri)

    print(
        "\n\n----------\n\nAll text has been collected and analysed. The process took {:0.2f} seconds.\n".format(time.time() - tāti_wā))  # Prints out how long the process took in a user friendly format

    return


if __name__ == '__main__':
    matua()
