from distutils.core import setup
setup(name='taumahi',
      version='1.1',
      py_modules=['taumahi'],
      data_files={('txtfiles': ['taumahi_txt/*.txt'])}
      )

# Uninstall:
# cd ~/../../usr/local/lib/python3.4/dist-packages \ sudo rm -r taumahi*
