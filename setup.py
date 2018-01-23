from distutils.core import setup
import sys

setup(name='taumahi',
      version='1.2',
      py_modules=['taumahi'],
      data_files=[('lib/python{}/dist-packages/taumahi_tūtira'.format(sys.version[0:3]), ['taumahi_tūtira/kupu_kino_kūare_tohutō.txt', 'taumahi_tūtira/kupu_kino.txt',
                                                                                          'taumahi_tūtira/kupu_rangirua_kūare_tohutō.txt', 'taumahi_tūtira/kupu_rangirua.txt'])]
      )

# Uninstall:
# cd ~/../../usr/local/lib/python3.*/dist-packages ; sudo rm -r taumahi*
