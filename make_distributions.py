#!python3.3
# -*- coding: utf-8 -*-
'''
Created on 05/08/2013

@author: Rodney
'''

if __name__ == "__main__":
    import os
    os.system("py setup.py bdist upload")
    os.system("py setup.py bdist --plat-name=win32 --format=wininst upload")
    os.system("py setup.py sdist upload")

