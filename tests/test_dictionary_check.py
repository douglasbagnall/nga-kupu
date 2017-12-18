import context
import taumahi


def test_māori_word():
    assert taumahi.hihira_raupapa_kupu('kupu')


def test_māori_uppercase():
    assert taumahi.hihira_raupapa_kupu('KUPU')


def test_english_word():
    assert not taumahi.hihira_raupapa_kupu('mittens')


def test_tohutō():
    assert taumahi.hihira_raupapa_kupu('rōpū')


def test_ignore_tohutō():
    assert not taumahi.hihira_raupapa_kupu('ropu', False)


def test_check_list():
    assert taumahi.hihira_raupapa(['kupu', 'cheese']) == (['kupu'], ['cheese'])


def test_waitangi():
    assert taumahi.hihira_raupapa_kupu('Waitangi')


def test_space():
    assert not taumahi.hihira_raupapa_kupu(' Pōneke')


def test_hihira_raupapa_kupu():
    assert not taumahi.hihira_raupapa_kupu('ae', False)


def test_whakatakitahi_tūtira():
    assert taumahi.hōputu(['ngawha', 'Wha', 'Nga'], True, True) == [
        'ŋaƒa', 'Ƒa', 'Ŋa']


def test_whakatakitahi_tūtira():
    assert taumahi.hōputu(['ŋaƒa', 'Ƒa', 'Ŋa'], True, False) == [
        'ngawha', 'Wha', 'Nga']


def test_whakatakitahi_kupu():
    assert taumahi.hōputu('ngawha', False, True) == 'ŋaƒa' and taumahi.hōputu(
        'Wha', False, True) == 'Ƒa' and taumahi.hōputu('Nga', False, True) == 'Ŋa'


def test_whakatakitahi_tūtira():
    assert taumahi.hōputu('ŋaƒa', False, False) == 'ngawha' and taumahi.hōputu(
        'Ƒa', False, False) == 'Wha' and taumahi.hōputu('Ŋa', False, False) == 'Nga'
