from distutils.core import setup
setup(name='taumahi',
      version='1.1',
      py_modules=['taumahi'],
      data_files=[('taumahi_txt', ['taumahi_txt/kupu_kino_no_tohutō.txt', 'taumahi_txt/kupu_kino.txt',
                                   'taumahi_txt/kupu_rangirua_no_tohutō.txt', 'taumahi_txt/kupu_rangirua.txt'])]
      )

# Uninstall:
# cd ~/../../usr/local/lib/python3.*/dist-packages \ sudo rm -r taumahi*
