from taumahi import dictionary_check_word, dictionary_check, poro_tūtira


def test_māori_word():
    assert dictionary_check_word('kupu')


def test_māori_uppercase():
    assert dictionary_check_word('KUPU')


def test_english_word():
    assert not dictionary_check_word('mittens')


def test_tohutō():
    assert dictionary_check_word('rōpū')


def test_ignore_tohutō():
    assert not dictionary_check_word('ropu', ignore_tohutō=False)


def test_check_list():
    assert dictionary_check(['kupu', 'cheese']) == (['kupu'], ['cheese'])


def test_waitangi():
    assert dictionary_check_word('Waitangi')


def test_space():
    assert not dictionary_check_word(' Pōneke')


def test_stop_list():
    assert poro_tūtira(['aia']) == []
