import context
import taumahi

def test_māori_word():
    assert taumahi.dictionary_check_word('kupu')


def test_māori_uppercase():
    assert taumahi.dictionary_check_word('KUPU')


def test_english_word():
    assert not taumahi.dictionary_check_word('mittens')


def test_tohutō():
    assert taumahi.dictionary_check_word('rōpū')


def test_ignore_tohutō():
    assert not taumahi.dictionary_check_word('ropu', ignore_tohutō=False)


def test_check_list():
    assert taumahi.dictionary_check(['kupu', 'cheese']) == (['kupu'], ['cheese'])


def test_waitangi():
    assert taumahi.dictionary_check_word('Waitangi')


def test_space():
    assert not taumahi.dictionary_check_word(' Pōneke')

def test_dictionary_check_word():
    assert not taumahi.dictionary_check_word('ae')
