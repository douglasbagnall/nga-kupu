# nga-kupu
Identify Māori words in text - still a work in progress
Some of these files are for the `nga-tautohetohe` project

Both scripts have only been tested on python3.

`kupu_tūtira.py` takes a multilingual corpus and returns a list of the words that it considers to be Māori, as well as hyphenated words. It is passed two filenames in the terminal, the first file containing the corpus, the second being the output file. It also determines how much of the text is Māori. Executing this script will be of the following format.

`python3 kupu_tūtira.py input_file.txt output_file.txt`

`dictionarycheck.py` takes a multilingual corpus and returns two lists. One list of words that are considered to be Māori, and another list of words that are of Māori form (consonant-vowel format, no doubling of consonants, always ends in a vowel, Māori alphabet), but are not considered to be Māori words. It checks them all against http://maoridictionary.co.nz

`englishwords.txt` is a text file that will soon be incorporated into `kupu_tūtira.py` in order to better scrutinise Māori words. It has been passed through `kupu_tūtira.py` and `dictionarycheck.py` and is the list of Māori form undefined words from a corpus of approximately 15 million English words.

# Next steps:
- incorporating the list of exceptions into `kupu_tūtira.py`
- making the percentage of Māori words function of `kupu_tūtira.py` into its own script
