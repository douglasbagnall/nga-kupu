# import libraries
import csv
from urllib.request import urlopen
import re
from bs4 import BeautifulSoup as bs
from datetime import datetime


class Transcript:
    def __init__(self, url, wā, title, ingoa_kaikōrero, count, kōrero_waenga):
        ''' Generate a transcript object with basic params '''
        self.url = url
        self.wā = wā
        self.title = title
        self.ingoa_kaikōrero = ingoa_kaikōrero
        self.count = count
        self.kōrero_waenga = kōrero_waenga

    def listify(self):
        return [
            self.url,
            self.wā,
            self.title,
            self.ingoa_kaikōrero,
            self.count,
            self.kōrero_waenga
        ]


class HansardTuhingaScraper:
    def __init__(self, url):
        ''' Set up our tuhituhi CorpusCollector with basic params '''
        self.url = url
        self.hanga_hupo(url)

    def hanga_hupo(self, url):
        # query the website and parse the returned html using beautiful soup
        self.soup = bs(urlopen(self.url), 'html.parser')

        self.kōrero_hupo = self.soup.find('div', attrs={'class': 'section'})

        self.meta_url = '{}{}'.format('https://www.parliament.nz', self.soup.find(
            'a', attrs={'class': 'metadata-link'})['href'])

        # Make soup from hansard metadata
        self.metasoup = bs(urlopen(self.meta_url), 'html.parser').table

    def horoi_transcript_factory(self):

        meta_entries = self.metasoup.find_all('td')
        wā = meta_entries[1].get_text()
        title = meta_entries[0].get_text()
        ingoa_kaikōrero = meta_entries[6].get_text()

        transcripts = []
        count = 0

        for paragraph in self.kōrero_hupo.find_all('p'):
            count += 1

            transcripts.append(Transcript(url=self.url.strip(),
                                          wā=wā,
                                          title=title,
                                          ingoa_kaikōrero=ingoa_kaikōrero,
                                          count=count,
                                          kōrero_waenga=paragraph.contents))

        # kōrero_katoa = '\n'.join([re.sub(r'[,.?!:"\']', '', sentence).strip() for sentence in re.findall(r'.+(?=[.?!:])', )])

        print('{}: {}\n{}\n'.format(wā, title, ingoa_kaikōrero))

        return transcripts


class CorpusAggregator:
    def __init__(self, url_list):
        ''' Set up our tuhituhi CorpusCollector with basic params '''
        self.url_list = url_list
        self.transcripts = []

        filename = "hansardcorpus.csv"

        with open(filename, 'w') as kiwaho:
            hansard_csv = csv.writer(kiwaho)
            # write the header
            hansard_csv.writerow([
                'url',
                'wā',
                'title',
                'ingoa_kaikōrero',
                'paragraph_number',
                'kōrero_waenga'
            ])
            for url in url_list:
                transcripts = HansardTuhingaScraper(
                    url).horoi_transcript_factory()
                for transcript in transcripts:
                    hansard_csv.writerow(transcript.listify())

                print('---\n')

                self.transcripts.append(transcripts)


def main():

    url_list = []

    url_library = 'zotero_hansardlibrary.csv'

    with open(url_library, 'r') as kiroto:
        zetero_csv = csv.DictReader(kiroto)
        for row in zetero_csv:
            url_list.append(row['Url'])  # Read the Url column

    corpus = CorpusAggregator(url_list)

    print('{} corpus compilation successful\n'.format(url_library))


if __name__ == '__main__':
    main()
