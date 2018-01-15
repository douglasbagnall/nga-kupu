# nga-kupu
[![Build Status](https://travis-ci.org/TeHikuMedia/nga-kupu.svg?branch=master)](https://travis-ci.org/TeHikuMedia/nga-kupu)

Identify Māori words in text.

All scripts are only intended for python3.
To install the package, run `python3 setup.py install` from the working directory

`auaha_tūtira_tū` creates the stoplists used in the `kōmiri_kupu` function (which is called in the `kupu_tūtira` script) from a user-provided English corpus. However I have provided such lists in a subfolder referenced throughout the code called `taumahi_tūtira`, created from Google's provided list of 20,000 most commonly used English words. You may recreate these lists from the same corpus or make your own by executing the script thusly.

`python3 auaha_tūtira_tū -i input_file`

`kupu_tūtira` takes a multilingual corpus and returns a list of the words that it considers to be Māori, as well as hyphenated words. It is passed two filenames in the terminal, the first file containing the corpus, the second being the output file. It also determines how much of the text is Māori. Use the following format to execute this script.

`python3 kupu_tūtira -i input_file.txt -o output_file.txt`

`hihira_raupapa` takes a multilingual corpus and returns two lists. One list of words that are considered to be Māori, and another list of words that are of Māori form (consonant-vowel format, no doubling of consonants, always ends in a vowel, Māori alphabet), but are not considered to be Māori words. It checks them all against http://maoridictionary.co.nz . Use the following format to execute this script.

`python3 hihira_raupapa -i input_file.txt -g output_file1.txt -b output_file2.txt`
