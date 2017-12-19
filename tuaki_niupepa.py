# import libraries
import csv
import re
import time
from pathlib import Path
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from datetime import datetime
from taumahi import kupu_ratios

taukaea_niupepa = 'http://www.nzdl.org/gsdlmod?gg=text&e=p-00000-00---off-0niupepa--00-0----0-10-0---0---0direct-10---4-------0-1l--11-en-50---20-about---00-0-1-00-0-0-11-1-0utfZz-8-00'
taukaea_niupepa_haurua = '{}{}'.format(
    taukaea_niupepa, '-0-0-11-10-0utfZz-8-00&a=d&c=niupepa&cl=CL1')


class NiupepaWhakatuaki:
    def __init__(self, taukaea_tuhinga):
        ''' Set up our tuhituhi CorpusCollector with basic params '''
        self.taukaea_tuhinga = taukaea_tuhinga
        self.hanga_hupo()

    def hanga_hupo(self):
        # query the website and parse the returned html using beautiful soup

        doc_id = self.taukaea_tuhinga.split('/')[6]
        alternative_URL = '{}{}'.format(taukaea_niupepa_haurua, doc_id)
        get_stuff = ''
        exception_flag = None

        try:
            get_stuff = urlopen('{}{}'.format(
                taukaea_niupepa, self.taukaea_tuhinga))
        except Exception as e:
            print(e, '\nTrying alternative URL...')
            try:
                get_stuff = urlopen(alternative_URL)
                exception_flag = True
                print('\nSuccess!\n')
            except Exception as e:
                raise Exception(e, '\nCould not find data')

        self.soup = bs(get_stuff, 'html.parser')

        self.retreived = datetime.now()

        if exception_flag:
            self.kōrero_hupo = self.soup.find('div', attrs={'class': 'section'}).select(
                'div.section > div.section')
        elif re.match(r'\d', doc_id):
            self.kōrero_hupo = self.soup.select('div.Hansard > div')
        else:
            self.kōrero_hupo = self.soup.find_all(
                'div', attrs={'class': 'section'})

        # Make soup from hansard metadata
        meta_url = '{}{}'.format(alternative_URL, '/metadata')
        self.metasoup = bs(urlopen(meta_url), 'html.parser').table

    def horoi_transcript_factory(self):

        meta_entries = self.metasoup.find_all('td')

        taukaea_tuhinga = '{}{}'.format(taukaea_niupepa, self.taukaea_tuhinga)
        wā = meta_entries[1].get_text()
        title = meta_entries[0].get_text()

        transcripts = []
        teReo_size = 0
        ambiguous_size = 0
        total_size = 0
        awaiting_teReo = None
        section_count = 0

        print('\n{}\n'.format(taukaea_tuhinga))

        for section in self.kōrero_hupo:

            section_count += 1
            # print('section:', section_count)
            paragraph_count = 0

            ingoa_kaikōrero = ''

            p_list = section.find_all('p')
            print('Paragraphs =', len(p_list))

            for paragraph in p_list:

                # print('paragraph: ', paragraph_count)

                strong_tags = paragraph.find_all('strong')

                flag = False

                for strong in strong_tags:
                    string = strong.extract().string
                    if not flag and string and re.search(r'[a-zA-Z]{5,}', string):
                        ingoa_kaikōrero = string.strip()
                        flag = True

                kōrero_waenga = paragraph.get_text(strip=True)

                if flag:
                    # p = re.search(r'(?<=:).*', kōrero_waenga)
                    p = kōrero_waenga.split(':', 1)[-1].strip()
                    if p:
                        kōrero_waenga = p

                if re.search(r'[a-zA-Z]', kōrero_waenga):
                    paragraph_count += 1

                    save_corpus, numbers = kupu_ratios(kōrero_waenga)

                    teReo_size += numbers[0]
                    ambiguous_size += numbers[1]
                    other_size += numbers[2]

                    if not save_corpus:
                        awaiting_teReo = re.match(
                            r'\[Authorised Te Reo text', text)
                        if awaiting_teReo:
                            save_corpus = True

                    if save_corpus:
                        print('{}: {}\nsection {}, paragraph {}, Maori = {}%\nname:{}\n{}\n'.format(
                            wā, title, section_count,
                            paragraph_count, heMāori, ingoa_kaikōrero, kōrero_waenga))
                        transcripts.append([taukaea_tuhinga, wā, title, section_count, paragraph_count,
                                            ingoa_kaikōrero] + numbers + [kōrero_waenga])
        print('Time:', self.retreived)
        doc_record = [self.retreived, self.taukaea_tuhinga, wā, title, teReo_size, ambiguous_size,
                      other_size, teReo_size / other_size, awaiting_teReo]
        return transcripts, doc_record


def tuaki_taukaea_niupepa():
    kōnae_ingoa = 'taukaea_kuputohu.csv'

    has_header = False
    taukaea_tuhinga_tūtira = []

    if Path(kōnae_ingoa).exists():
        with open(kōnae_ingoa, 'r') as kōnae:
            for row in csv.DictReader(kōnae):
                taukaea_tuhinga_tūtira.append(row['url'])
    else:
        with open(kōnae_ingoa, 'w') as kōnae:
            csv.writer(kōnae).writerow(['Date retreived', 'url'])

    taukaea_tauhiku = ''
    if taukaea_tuhinga_tūtira:
        taukaea_tauhiku = taukaea_tuhinga_tūtira[-1]
    tūtira_hou = tiki_taukaea_hou(taukaea_tauhiku)

    with open(kōnae_ingoa, 'a') as kōnae:
        url_writer = csv.writer(kōnae)
        for url in reversed(tūtira_hou):
            taukaea_tuhinga_tūtira.append(url[1])
            url_writer.writerow(url)

    print('\nCollected all URLs\n')

    return taukaea_tuhinga_tūtira


def tiki_taukaea_hou(taukaea_tauhiku):
    hupa = bs(urlopen('{}{}'.format(
        taukaea_niupepa, '-0-0-11-10-0utfZz-8-00&a=d&c=niupepa&cl=CL1')), 'html.parser')

    tūtira_hou = []
    while True:
        print('\nChecking for new newspaper\n')

        retreivedtime = datetime.now()
        for h2 in hupa.select('ul.hansard__list h2'):
            new_url = h2.a['href']
            if new_url == taukaea_tauhiku:
                return tūtira_hou
            else:
                print(new_url)
                tūtira_hou.append([retreivedtime, new_url])

        next_page = hupa.find(
            'li', attrs={'class', 'pagination__next'})

        if next_page:
            next_url = '{}{}'.format(taukaea_niupepa, next_page.find(
                'a')['href'])
            hupa = bs(urlopen(next_url), 'html.parser')
        else:
            return tūtira_hou


def aggregate_hansard_corpus(taukaea_tuhingas):
    transcripts = []

    corpusfilename = 'hansardcorpus.csv'
    recordfilename = 'hansardrecord.csv'

    record_list = []
    waiting_for_reo_list = []

    if Path(recordfilename).exists():
        with open(recordfilename, 'r') as record_file:
            rowcount = 0
            for row in csv.DictReader(record_file):
                record_list.append(row)
                if row['awaiting authorised reo'] is True:
                    waiting_for_reo_list.append(rowcount)
                rowcount += 1
    else:
        with open(recordfilename, 'w') as record_file:
            head_writer = csv.writer(record_file)
            head_writer.writerow([
                'Date retreived',
                'Hansard document url',
                'wā',
                'title',
                'Te Reo length',
                'Ambiguous length'
                'Other length',
                'is Māori (%)',
                'awaiting authorised reo'
            ])

        # corpus_list = []

    if not Path(corpusfilename).exists():
        #     with open(corpusfilename, 'r') as corpus:
        #         if corpus_has_header:
        #             for row in csv.DictReader(corpus):
        #                 record_list.append(row)
        # else:
        with open(corpusfilename, 'w') as corpus:
            head_writer = csv.writer(corpus)
            head_writer.writerow([
                'Hansard document url',
                'wā',
                'title',
                'section number',
                'utterance number',
                'ingoa kaikōrero',
                'Te Reo length',
                'Ambiguous length'
                'Other length',
                'is Māori (%)',
                'kōrero waenga'
            ])

    remaining_urls = []

    if record_list:
        last_record_url = record_list[-1]['Hansard document url']
        remaining_urls = taukaea_tuhingas[taukaea_tuhingas.index(
            last_record_url) + 1:]
    else:
        remaining_urls = taukaea_tuhingas

    with open(recordfilename, 'a') as record:
        with open(corpusfilename, 'a') as kiwaho:
            record_csv = csv.writer(record)
            hansard_csv = csv.writer(kiwaho)

            for taukaea_tuhinga in remaining_urls:
                corpus_writer(taukaea_tuhinga, record_csv, hansard_csv)

                print('---\n')


def corpus_writer(taukaea_tuhinga, record_csv, hansard_csv):
    transcripts, doc_record = NiupepaWhakatuaki(
        taukaea_tuhinga).horoi_transcript_factory()

    record_csv.writerow(doc_record)
    if transcripts:
        for transcript in transcripts:
            hansard_csv.writerow(transcript)


def main():

    start_time = time.time()

    hansard_taukaea_tuhingas = tuaki_taukaea_niupepa()

    aggregate_hansard_corpus(hansard_taukaea_tuhingas)

    print('Corpus compilation successful\n')
    print("\n--- Job took %s seconds ---\n" % (time.time() - start_time))


if __name__ == '__main__':
    main()
