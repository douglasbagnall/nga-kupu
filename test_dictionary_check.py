from taumahi import dictionary_check_word, dictionary_check
def test_māori_word():
    assert dictionary_check_word('kupu')

def test_māori_uppercase():
    assert dictionary_check_word('KUPU')

def test_english_word():
    assert not dictionary_check_word('mittens')

def test_tohutō():
    assert dictionary_check_word('rōpū')

def test_no_tohutō():
    assert not dictionary_check_word('ropu')

def test_ignore_tohutō():
    assert dictionary_check_word('ropu', ignore_tohutō=True)

def test_check_list():
    assert dictionary_check(['kupu', 'cheese']) == (['kupu'], ['cheese'])
