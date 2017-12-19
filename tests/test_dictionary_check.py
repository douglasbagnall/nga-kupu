import context
import taumahi


def test_māori_word():
    assert taumahi.hihira_raupapa_kupu('kupu', True)


def test_māori_uppercase():
    assert taumahi.hihira_raupapa_kupu('KUPU', True)


def test_english_word():
    assert not taumahi.hihira_raupapa_kupu('mittens', True)


def test_tohutō():
    assert taumahi.hihira_raupapa_kupu('rōpū', True)


def test_ignore_tohutō():
    assert not taumahi.hihira_raupapa_kupu('ropu', False)


def test_check_list():
    assert taumahi.hihira_raupapa(['kupu', 'cheese']) == (['kupu'], ['cheese'])


def test_waitangi():
    assert taumahi.hihira_raupapa_kupu('Waitangi', True)


def test_space():
    assert not taumahi.hihira_raupapa_kupu(' Pōneke', True)


def test_hihira_raupapa_kupu():
    assert not taumahi.hihira_raupapa_kupu('ae', False)


def test_whakatakitahi_tūtira():
    assert taumahi.hōputu(['ngawha', 'Wha', 'Nga'], True) == [
        'ŋaƒa', 'Ƒa', 'Ŋa']


def test_whakatakirua_tūtira():
    assert taumahi.hōputu(['ŋaƒa', 'Ƒa', 'Ŋa'], False) == [
        'ngawha', 'Wha', 'Nga']


def test_whakatakitahi():
    assert taumahi.hōputu('ngawha', True) == 'ŋaƒa' and taumahi.hōputu('Wha', True) == 'Ƒa' and taumahi.hōputu(
        'Nga', True) == 'Ŋa' and taumahi.hōputu('WHA', True) == 'ƑA' and taumahi.hōputu('NGA', True) == 'ŊA'


def test_whakatakirua():
    assert taumahi.hōputu('ŋaƒa', False) == 'ngawha' and taumahi.hōputu('Ƒa', False) == 'Wha' and taumahi.hōputu(
        'Ŋa', False) == 'Nga' and taumahi.hōputu('ƑA', False) == 'WhA' and taumahi.hōputu('ŊA', False) == 'NgA'
