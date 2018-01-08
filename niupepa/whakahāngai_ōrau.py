import csv
import argparse
from taumahi import *
from pandas import read_csv
from tuaki_niupepa_hou import tiki_ōrau


def whakahāngi_kōnae(perehitanga_kōnae_ingoa, perehitanga_kōnae_ingoa_hou):
    # Updates the Māori percentage estimate for the raw text in an existing csv for text scraped from the Māori newspaper website

    with open(perehitanga_kōnae_ingoa, 'r') as kōnae:
        kōnae_tūtira = list(csv.reader(kōnae))
        kōnae.close()

    with open(perehitanga_kōnae_ingoa_hou, 'w') as kōnae:
        perehitanga_kuputohu = csv.writer(kōnae)
        perehitanga_kuputohu.writerow(kōnae_tūtira[0])
        for rārangi in kōnae_tūtira[1:]:
            print(rārangi[0:4])
            ōrau = tiki_ōrau(rārangi[5])
            perehitanga_kuputohu.writerow(rārangi[0:4] + [ōrau, rārangi[5]])
        kōnae.close()


if __name__ == '__main__':
    whakatukai = argparse.ArgumentParser()
    whakatukai.add_argument(
        '--input', '-i', help="Input csv file to be sorted")
    whakatukai.add_argument(
        '--output', '-o', help="Output text file where sorted input file is to be stored")
    whakatukai.add_argument(
        '--update', '-u', help="Input file to be sorted and saved under the same name")
    kōwhiri = whakatukai.parse_args()

    if kōwhiri.update:
        perehitanga_kōnae_ingoa = perehitanga_kōnae_ingoa_hou = kōwhiri.update

    else:
        perehitanga_kōnae_ingoa = kōwhiri.input if kōwhiri.input else 'perehitanga_kuputohu.csv'
        perehitanga_kōnae_ingoa_hou = kōwhiri.output if kōwhiri.output else 'test.csv'

    whakahāngi_kōnae(perehitanga_kōnae_ingoa, perehitanga_kōnae_ingoa_hou)
