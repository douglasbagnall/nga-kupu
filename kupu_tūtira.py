#returns a list of all māori words and tells the user what percentage of words are considered 'english' or 'māori'

import re
import sys
kōnae_mai = sys.argv[1]
kōnae_atu = sys.argv[2]

def tangohia_kupu_tōkau():
    # opening the file and reading it to one long string of lowercase characters
    kōnae = open(kōnae_mai, "r")
    kupu_tōkau = kōnae.read().lower()
    kōnae.close()
    return kupu_tōkau

def whakatū_aho():
    #strings of unicode characters, vowels consonants and non-māori letters, used to distinguish the english words from māori words
    return "aāeēiīoōuū", "hkmnprtwŋf", "bcdfjlqsvxyz"

def raupapa_tohu(oropurae, orokati, kupu_hou):
    #creates dictionaries for ordering the māori alphabet from the vowel and consonant strings
    arapū = oropurae + orokati
    papakupu_kī = "ABCDEFGHIJKLMNOPQRST"
    papakupu_whakamua = {kī:papakupu_kī[wāriutanga - 1] for wāriutanga, kī in enumerate(arapū, 1)}
    papakupu_whakamuri = {papakupu_kī[kī - 1]:wāriutanga for kī, wāriutanga in enumerate(arapū, 1)}

    #sorts into māori alphabetical order
    for arapū_pūriki in arapū:
        kupu_hou = [re.sub(arapū_pūriki, papakupu_whakamua[arapū_pūriki], kupu) for kupu in kupu_hou]

    kupu_hou.sort()

    for tau in range(len(arapū)):
        kupu_hou = [re.sub(papakupu_kī[tau], papakupu_whakamuri[papakupu_kī[tau]], kupu) for kupu in kupu_hou]

    return kupu_hou

def auaha_kupu_tūtira(kupu_tōkau):
    #creates a list of all words in the file string that contain english and/or māori letters, and one of all hyphenated words
    kupu_tūtira = re.findall(r'[a-zāēīōū]+', kupu_tōkau)
    kupu_pāhekoheko = re.findall(r'(?!-)(?![a-zāēīōū-]*--[a-zāēīōū-]*)(?![a-zāēīōū-]*[hkmnprtwg]-)([a-zāēīōū-]+)(?<!-)', kupu_tōkau)
    print(len(kupu_tūtira))
    print(len(kupu_pāhekoheko))
    #combines the lists, removes duplicates by transforming into a set and back again
    kupu_tūtira_pīki = list(set(kupu_tūtira + kupu_pāhekoheko))
    return kupu_tūtira_pīki

def poro_tūtira(oropurae, orokati, pūriki_pākehā, kupu_tūtira_pīki):
    #removes words that contain any english characters from the string above
    kupu_hou = [kupu for kupu in kupu_tūtira_pīki if not any(pūriki in kupu for pūriki in pūriki_pākehā)]

    #replaces 'ng' and 'wh' with 'ŋ' and 'f' respectively, since words with english characters have been removed and it is easier to deal with in unicode format
    kupu_hou = [re.sub(r'ng', 'ŋ', kupu) for kupu in kupu_hou]
    kupu_hou = [re.sub(r'wh', 'f', kupu) for kupu in kupu_hou]
    #removes words that have english words with māori characters (like "the"), words that end in a consonant, or words with a 'g' that is not preceeded by an 'n'
    kupu_hou = [kupu for kupu in kupu_hou if not (re.compile(r'[fhkmnŋprtw][fhkmnŋprtw]').search(kupu) or (kupu[-1] in orokati) or ("g" in kupu))]

    kupu_hou = raupapa_tohu(oropurae, orokati, kupu_hou)

    #returns the letters to traditional format from unicode format
    kupu_hou = [re.sub(r'ŋ', 'ng', kupu) for kupu in kupu_hou]
    kupu_hou = [re.sub(r'f', 'wh', kupu) for kupu in kupu_hou]

    return kupu_hou

def tuhi_puta_tuhinga(kupu_hou):
    #writes the list of words to a new document, each word and hyphenated word on a new line
    kupu_tūtira_hou = open(kōnae_atu,"w")
    kupu_tōkau_pīki = "\n".join(kupu_hou)
    kupu_tūtira_hou.write(kupu_tōkau_pīki)
    kupu_tūtira_hou.close()

def tatau_tupu(kupu_tūtira_pīki, kupu_hou):
    percentage = round(float(len(kupu_hou)) / float(len(kupu_tūtira_pīki)) * 100, 2)
    print("This text is " + str(percentage) + "% Māori")

def matua():
    kupu_tōkau = tangohia_kupu_tōkau()
    oropurae, orokati, pūriki_pākehā = whakatū_aho()
    kupu_tūtira_pīki = auaha_kupu_tūtira(kupu_tōkau)
    kupu_hou = poro_tūtira(oropurae, orokati, pūriki_pākehā, kupu_tūtira_pīki)
    tuhi_puta_tuhinga(kupu_hou)
    tatau_tupu(kupu_tūtira_pīki, kupu_hou)

if __name__=='__main__':
    matua()

