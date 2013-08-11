#!python3
# -*- coding: utf-8 -*-
#from distutils.core import setup

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

import sys

DISTUTILS_DEBUG = True

if DISTUTILS_DEBUG:
    import urllib.request
    v_request = urllib.request.urlopen('https://api.travis-ci.org/repos/Rod-Persky/pyIGES')
    v_request = str(v_request.read())
    v_request = v_request[v_request.find("last_build_number") + 20:]
    v_request = v_request[:v_request.find("\"")]
    version = int(v_request) + 1
    version = "0.0." + str(version)
    print(version)

    version_file = open("pyIGESVersion", 'w')
    version_file.write(version)
    version_file.close()

else:
    version_file = open("pyIGESVersion", 'r')
    version = version_file.read()
    version_file.close()


py_version = sys.version_info[:2]
PY3 = py_version[0] == 3

if not PY3:
    raise RuntimeError('Python 3.x is required')

with open('README.md') as file:
    long_description = file.read()

setup(
      name = 'pyIGES',
      version = version,  # major.minor.revision

      platforms = ['Linux', 'Windows'],
      url = 'https://github.com/Rod-Persky/pyIGES',

      classifiers = [
        'Development Status :: 3 - Alpha',

        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Visualization',

        'License :: OSI Approved :: Academic Free License (AFL)',

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",

        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: Science/Research',

        'Environment :: Console',
        'Environment :: No Input/Output (Daemon)',  # No IO required

        'Natural Language :: English',

        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: OS Independent',
        ],

      description = 'Python IGES geometry export system',
      long_description = long_description,
      license = 'Academic Free License ("AFL") v. 3.0',

      author = 'Rodney Persky',
      author_email = 'rodney.persky@gmail.com',

      packages = ['pyiges'],
      package_dir = {'pyiges': 'pyiges'},
      zip_safe = True,

      # Cannot automatically download from UCI at present due to filtering or some such
      dependency_links = [#'http://www.lfd.uci.edu/~gohlke/pythonlibs/chxm2uxu/numpy-MKL-1.7.1.win-amd64-py3.3.exe',
                          #'http://www.lfd.uci.edu/~gohlke/pythonlibs/chxm2uxu/numpy-MKL-1.7.1.win32-py3.3.exe',
                          #'http://www.lfd.uci.edu/~gohlke/pythonlibs/chxm2uxu/scipy-0.12.0.win-amd64-py3.3.exe',
                          #'http://www.lfd.uci.edu/~gohlke/pythonlibs/chxm2uxu/scipy-0.12.0.win32-py3.3.exe'
                          'http://www.lfd.uci.edu/~gohlke/pythonlibs/chxm2uxu'
                          ],

      include_package_data = True,

      py_modules = ['ez_setup']

      )
