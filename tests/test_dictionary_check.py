import context
from taumahi import *


def test_māori_word():
    assert hihira_raupapa_kupu('kupu', True)


def test_māori_uppercase():
    assert hihira_raupapa_kupu('KUPU', True)


def test_english_word():
    assert not hihira_raupapa_kupu('mittens', True)


def test_tohutō():
    assert hihira_raupapa_kupu('rōpū', True)


def test_ignore_tohutō():
    assert not hihira_raupapa_kupu('ropu', False)


def test_check_list():
    assert hihira_raupapa(['kupu', 'cheese']) == (['kupu'], ['cheese'])


def test_waitangi():
    assert hihira_raupapa_kupu('Waitangi', True)


def test_space():
    assert not hihira_raupapa_kupu(' Pōneke', True)


def test_hihira_raupapa_kupu():
    assert not hihira_raupapa_kupu('ae', False)


def test_whakatakitahi_tūtira():
    assert hōputu(['ngawha', 'Wha', 'Nga'], True) == [
        'ŋaƒa', 'Ƒa', 'Ŋa']


def test_whakatakirua_tūtira():
    assert hōputu(['ŋaƒa', 'Ƒa', 'Ŋa'], False) == [
        'ngawha', 'Wha', 'Nga']


def test_whakatakitahi():
    assert hōputu('ngawha', True) == 'ŋaƒa' and hōputu('Wha', True) == 'Ƒa' and hōputu(
        'Nga', True) == 'Ŋa' and hōputu('WHA', True) == 'ƑA' and hōputu('NGA', True) == 'ŊA'


def test_whakatakirua():
    assert hōputu('ŋaƒa', False) == 'ngawha' and hōputu('Ƒa', False) == 'Wha' and hōputu(
        'Ŋa', False) == 'Nga' and hōputu('ƑA', False) == 'WhA' and hōputu('ŊA', False) == 'NgA'
