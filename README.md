# nga-kupu
Identify Māori words in text.

Both scripts have only been tested on python3.
To install the package, run "python3 setup.py install" from the working directory

`kupu_tūtira` takes a multilingual corpus and returns a list of the words that it considers to be Māori, as well as hyphenated words. It is passed two filenames in the terminal, the first file containing the corpus, the second being the output file. It also determines how much of the text is Māori. Use the following format to execute this script.

`python3 kupu_tūtira.py -i input_file.txt -o output_file.txt`

`dictionarycheck` takes a multilingual corpus and returns two lists. One list of words that are considered to be Māori, and another list of words that are of Māori form (consonant-vowel format, no doubling of consonants, always ends in a vowel, Māori alphabet), but are not considered to be Māori words. It checks them all against http://maoridictionary.co.nz . Use the following format to execute this script.

`python3 dictionarycheck.py -i input_file.txt -g output_file1.txt -b output_file2.txt`

`englishwords.txt` is a text file that will soon be incorporated into `kupu_tūtira.py` in order to better scrutinise Māori words. It has been passed through `kupu_tūtira.py` and `dictionarycheck.py` and is the list of Māori form undefined words from a corpus of approximately 15 million English words.
