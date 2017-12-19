from distutils.core import setup
setup(name='taumahi',
      version='1.1',
      packages=['taumahi'],
      package_dir={'taumahi': 'taumahi'},
      package_data={'taumahi': ['*.txt']}
      )

# Uninstall:
# cd ~/../../usr/local/lib/python3.4/dist-packages
# sudo rm -r taumahi*
